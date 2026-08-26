# -*- coding: utf-8 -*-
"""Quote Follow-up Cadence models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuoteFollowup(models.Model):
    _name = 'sf.quote.followup'
    _description = 'Quote Follow-up'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    order_id = fields.Many2one('sale.order', string='Quotation', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    followup_step = fields.Selection([
        ('d3', 'Day 3'),
        ('d7', 'Day 7'),
        ('d14', 'Day 14'),
        ], string='Step', default=d3)
    due_date = fields.Date(string='Due Date')
    outcome = fields.Text(string='Outcome Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('contacted', 'Contacted'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.quote.followup') or 'NEW'
        return super().create(vals_list)

    def action_contacted(self):
        self.write({'state': 'contacted'})

    def action_won(self):
        self.write({'state': 'won'})

    def action_lost(self):
        self.write({'state': 'lost'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.quote.followup'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.quote.followup'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
