# -*- coding: utf-8 -*-
"""Quality Trend Dashboard Config models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_trend_dashboard(models.Model):
    _name = 'sf.quality_trend_dashboard'
    _description = 'Quality Trend Dashboard Config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    metric_name = fields.Char(string='Metric', required=True)
    metric_type = fields.Selection([
        ('defect_rate', 'Defect Rate'),
        ('first_pass_yield', 'First Pass Yield'),
        ('customer_complaints', 'Customer Complaints'),
        ('scrap_rate', 'Scrap Rate'),
        ], string='Type', required=True)
    target_value = fields.Float(string='Target')
    alert_threshold = fields.Float(string='Alert Threshold')
    trend_direction = fields.Selection([
        ('up', 'Increasing'),
        ('down', 'Decreasing'),
        ('stable', 'Stable'),
        ], string='Desired Trend', default=down)
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
                    'sf.quality_trend_dashboard') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

