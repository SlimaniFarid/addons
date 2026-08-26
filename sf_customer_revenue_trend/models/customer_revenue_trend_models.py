# -*- coding: utf-8 -*-
"""Customer Revenue Trend Alerts models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRevenueTrend(models.Model):
    _name = 'sf.revenue.trend'
    _description = 'Revenue Trend Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    period_current = fields.Date(string='Current Period', required=True)
    revenue_current = fields.Monetary(string='Current Revenue')
    revenue_previous = fields.Monetary(string='Previous Revenue')
    drop_percent = fields.Float(string='Drop %')
    action_taken = fields.Text(string='Action Taken')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('detected', 'Detected'),
        ('contacted', 'Contacted'),
        ('recovered', 'Recovered'),
        ('lost', 'Lost'),
        ], string='Status', default='detected', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.revenue.trend') or 'NEW'
        return super().create(vals_list)

    def action_contacted(self):
        self.write({'state': 'contacted'})

    def action_recovered(self):
        self.write({'state': 'recovered'})

    def action_lost(self):
        self.write({'state': 'lost'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.revenue.trend'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave2 ---
class _Wave2Trend(models.Model):
    _inherit = 'sf.revenue.trend'

    def action_refresh(self):
        """Current vs previous full-month invoiced revenue from posted
        customer invoices; drop% computed; auto-flag >20% drop."""
        self.ensure_one()
        Move = self.env['account.move']
        today = fields.Date.context_today(self)
        cur_start = today.replace(day=1)
        prev_end = cur_start - relativedelta(days=1)
        prev_start = prev_end.replace(day=1)

        def rev(d_from, d_to):
            moves = Move.search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('partner_id', '=', self.partner_id.id),
                ('invoice_date', '>=', d_from),
                ('invoice_date', '<=', d_to),
            ])
            return sum(moves.mapped('amount_untaxed_signed'))

        r_cur = abs(rev(cur_start, today))
        r_prev = abs(rev(prev_start, prev_end))
        drop = ((r_prev - r_cur) / r_prev * 100.0) if r_prev else 0.0
        self.write({
            'period_current': cur_start,
            'revenue_current': r_cur,
            'revenue_previous': r_prev,
            'drop_percent': round(drop, 1),
        })
        if drop > 20:
            self.message_post(body=_(
                'Revenue dropped %.1f%% vs last month (%s -> %s). '
                'Follow-up recommended.') % (drop, r_prev, r_cur))
        return True

    @api.model
    def cron_refresh_top_partners(self, limit=100):
        """Keep one trend record per top-revenue partner up to date."""
        Move = self.env['account.move']
        groups = Move._read_group(
            [('move_type', '=', 'out_invoice'), ('state', '=', 'posted')],
            ['partner_id'], aggregates=['amount_total:sum'])
        tops = sorted(groups, key=lambda g: -(g[1] or 0))[:limit]
        Trend = self.env['sf.revenue.trend']
        for partner, _amt in tops:
            rec = Trend.search([('partner_id', '=', partner.id)], limit=1)
            if not rec:
                rec = Trend.create({'partner_id': partner.id})
            rec.action_refresh()
