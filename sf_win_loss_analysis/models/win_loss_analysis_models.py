# -*- coding: utf-8 -*-
"""Win / Loss Analysis Library models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfWinLoss(models.Model):
    _name = 'sf.win.loss'
    _description = 'Win / Loss Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    outcome = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ], string='Outcome', required=True)
    primary_reason = fields.Selection([
        ('price', 'Price'),
        ('quality', 'Quality'),
        ('delay', 'Lead Time'),
        ('relationship', 'Relationship'),
        ('other', 'Other'),
        ], string='Primary Reason')
    competitor = fields.Char(string='Competitor')
    price_gap_percent = fields.Float(string='Price Gap %')
    lessons = fields.Html(string='Lessons Learned')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('analyzed', 'Analyzed'),
        ('shared', 'Shared'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.win.loss') or 'NEW'
        return super().create(vals_list)

    def action_analyzed(self):
        self.write({'state': 'analyzed'})

    def action_shared(self):
        self.write({'state': 'shared'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.win.loss'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave2 ---
class _Wave2(models.Model):
    _inherit = 'sf.win.loss'

    @api.model
    def action_analyze(self):
        """Aggregate win/loss KPIs across analysed records and broadcast."""
        recs = self.search([('outcome', 'in', ('won', 'lost'))])
        total = len(recs)
        won = len(recs.filtered(lambda r: r.outcome == 'won'))
        win_rate = (won / total * 100.0) if total else 0.0
        losses = recs.filtered(lambda r: r.outcome == 'lost')
        reasons = {}
        for reason in set(losses.mapped('primary_reason')):
            if reason:
                reasons[reason] = len(losses.filtered(
                    lambda r, rr=reason: r.primary_reason == rr))
        top = sorted(reasons.items(), key=lambda kv: -kv[1])[:3]
        gaps = [g for g in losses.mapped('price_gap_percent') if g]
        avg_gap = sum(gaps) / len(gaps) if gaps else 0.0
        body = (_('Win/Loss analysis: %s deals, win rate %.1f%%. '
                  'Top loss reasons: %s. Avg price gap on losses: %.1f%%.')
                % (total, win_rate,
                   ', '.join('%s (%d)' % kv for kv in top) or '-',
                   avg_gap))
        self.message_post(body=body)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': _('Win/Loss Analysis'),
                       'message': body, 'type': 'success'},
        }
