# -*- coding: utf-8 -*-
"""Recurring Management Fee Billing models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMgmtFee(models.Model):
    _name = 'sf.mgmt.fee'
    _description = 'Management Fee Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    client_id = fields.Many2one('res.partner', string='Client / Entity', required=True)
    fee_type = fields.Selection([
        ('aum', '% of AUM'),
        ('fixed', 'Fixed Monthly'),
        ('hourly', 'Hourly'),
        ], string='Fee Type', required=True)
    rate_percent = fields.Float(string='Rate %')
    fixed_amount = fields.Monetary(string='Fixed Amount')
    billing_day = fields.Integer(string='Billing Day', default=1)
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('ended', 'Ended'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.mgmt.fee') or 'NEW'
        return super().create(vals_list)

    def action_paused(self):
        self.write({'state': 'paused'})

    def action_ended(self):
        self.write({'state': 'ended'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.mgmt.fee'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
