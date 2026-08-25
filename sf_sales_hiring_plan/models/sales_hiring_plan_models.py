# -*- coding: utf-8 -*-
"""Sales Hiring Plan & Ramp Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_hiring_plan(models.Model):
    _name = 'sf.sales_hiring_plan'
    _description = 'Sales Hiring Plan & Ramp Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    position = fields.Char(string='Position', required=True)
    target_hire_date = fields.Date(string='Target Hire Date')
    ramp_months = fields.Integer(string='Ramp Time (months)', default=3)
    expected_quota = fields.Monetary(string='Expected Quota')
    fully_ramped_date = fields.Date(string='Fully Ramped Date')
    cost_per_hire = fields.Monetary(string='Cost per Hire')
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
                    'sf.sales_hiring_plan') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

