# -*- coding: utf-8 -*-
"""Quality Inspection Planner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_inspection_planner(models.Model):
    _name = 'sf.quality_inspection_planner'
    _description = 'Quality Inspection Planner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    inspection_point = fields.Char(string='Inspection Point', required=True)
    sampling_plan = fields.Char(string='Sampling Plan')
    frequency = fields.Selection([
        ('each', 'Each Piece'),
        ('hourly', 'Hourly'),
        ('shift', 'Per Shift'),
        ('daily', 'Daily'),
        ], string='Frequency', required=True)
    criteria = fields.Text(string='Acceptance Criteria')
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
                    'sf.quality_inspection_planner') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

