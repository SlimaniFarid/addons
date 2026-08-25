# -*- coding: utf-8 -*-
"""Inspection Plan Template models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_inspection_plan2(models.Model):
    _name = 'sf.quality_inspection_plan2'
    _description = 'Inspection Plan Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    operation = fields.Char(string='Operation / Step', required=True)
    inspection_type = fields.Selection([
        ('incoming', 'Incoming'),
        ('in_process', 'In-Process'),
        ('final', 'Final'),
        ], string='Type', required=True)
    sampling_plan = fields.Char(string='Sampling Plan')
    criteria = fields.Text(string='Acceptance Criteria')
    control_method = fields.Char(string='Control Method')
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
                    'sf.quality_inspection_plan2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

