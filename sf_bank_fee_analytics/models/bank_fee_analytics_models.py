# -*- coding: utf-8 -*-
"""Bank Fee Analytics models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBank_fee_analytics(models.Model):
    _name = 'sf.bank_fee_analytics'
    _description = 'Bank Fee Analytics'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    bank_account = fields.Char(string='Bank Account', required=True)
    period_month = fields.Date(string='Period', required=True)
    total_fees = fields.Monetary(string='Total Fees')
    fee_categories = fields.Html(string='Fee Breakdown')
    savings_note = fields.Text(string='Savings Opportunities')
    currency_id = fields.Many2one(related='company_id.currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.bank_fee_analytics') or 'NEW'
        return super().create(vals_list)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.bank_fee_analytics'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
