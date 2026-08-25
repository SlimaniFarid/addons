# -*- coding: utf-8 -*-
"""Sales Forecast Category Manager models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_forecast_category(models.Model):
    _name = 'sf.sales_forecast_category'
    _description = 'Sales Forecast Category Manager'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    category = fields.Selection([
        ('commit', 'Commit'),
        ('best_case', 'Best Case'),
        ('pipeline', 'Pipeline'),
        ('omitted', 'Omitted'),
        ], string='Category', required=True)
    criteria = fields.Text(string='Category Criteria', required=True)
    weight = fields.Float(string='Forecast Weight %')
    accuracy_target = fields.Float(string='Accuracy Target %')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.sales_forecast_category') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

