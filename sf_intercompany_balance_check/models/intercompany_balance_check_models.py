# -*- coding: utf-8 -*-
"""Intercompany Balance Check models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfIcBalanceCheck(models.Model):
    _name = 'sf.ic.balance.check'
    _description = 'IC Balance Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period_month = fields.Date(string='Period', required=True)
    company_a = fields.Char(string='Entity A', required=True)
    company_b = fields.Char(string='Entity B', required=True)
    balance_a_books = fields.Float(string='Balance in A Books')
    balance_b_books = fields.Float(string='Balance in B Books')
    difference = fields.Float(string='Difference')
    explanation = fields.Text(string='Discrepancy Explanation')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('explained', 'Explained'),
        ('resolved', 'Resolved'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.ic.balance.check') or 'NEW'
        return super().create(vals_list)

    def action_explained(self):
        self.write({'state': 'explained'})

    def action_resolved(self):
        self.write({'state': 'resolved'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.ic.balance.check'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.ic.balance.check'

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
