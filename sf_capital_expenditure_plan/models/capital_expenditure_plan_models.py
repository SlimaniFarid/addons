# -*- coding: utf-8 -*-
"""Multi-Year CapEx Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCapital_expenditure_plan(models.Model):
    _name = 'sf.capital_expenditure_plan'
    _description = 'Multi-Year CapEx Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    plan_year = fields.Integer(string='Plan Year', required=True)
    category = fields.Char(string='Category', required=True)
    planned_amount = fields.Monetary(string='Planned Amount')
    depreciation_years = fields.Integer(string='Depreciation Years', default=5)
    annual_dep = fields.Float(string='Annual Depreciation')
    currency_id = fields.Many2one(related='company_id.currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.capital_expenditure_plan') or 'NEW'
        return super().create(vals_list)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.capital_expenditure_plan'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
