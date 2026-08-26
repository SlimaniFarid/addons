# -*- coding: utf-8 -*-
"""Weekly Treasury Planning Board models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfTreasuryWeek(models.Model):
    _name = 'sf.treasury.week'
    _description = 'Treasury Week'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    week_start = fields.Date(string='Week Starting', required=True)
    opening_balance = fields.Monetary(string='Opening Balance', required=True)
    expected_inflows = fields.Monetary(string='Expected Inflows')
    expected_outflows = fields.Monetary(string='Expected Outflows')
    projected_close = fields.Monetary(string='Projected Close')
    decisions = fields.Text(string='Decisions / Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('locked', 'Locked'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.treasury.week') or 'NEW'
        return super().create(vals_list)

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

    def action_locked(self):
        self.write({'state': 'locked'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.treasury.week'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.treasury.week'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
