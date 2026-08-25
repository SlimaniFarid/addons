# -*- coding: utf-8 -*-
"""Automatic Accrual Reversal models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAccrual_reversal_auto(models.Model):
    _name = 'sf.accrual_reversal_auto'
    _description = 'Automatic Accrual Reversal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    accrual_ref = fields.Char(string='Original Accrual Ref', required=True)
    period = fields.Date(string='Original Period', required=True)
    reversal_period = fields.Date(string='Reversal Period')
    amount = fields.Monetary(string='Amount')
    auto_reversed = fields.Boolean(string='Auto-Reversed')
    currency_id = fields.Many2one(related='company_id.currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.accrual_reversal_auto') or 'NEW'
        return super().create(vals_list)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.accrual_reversal_auto'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
