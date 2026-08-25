# -*- coding: utf-8 -*-
"""Sales Content Library models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_content_library(models.Model):
    _name = 'sf.sales_content_library'
    _description = 'Sales Content Library'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Content Title', required=True)
    content_type = fields.Selection([
        ('battlecard', 'Battle Card'),
        ('case_study', 'Case Study'),
        ('roi_tool', 'ROI Calculator'),
        ('deck', 'Presentation Deck'),
        ], string='Type', required=True)
    usage_count = fields.Integer(string='Times Used')
    last_used = fields.Date(string='Last Used')
    effectiveness = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ], string='Effectiveness', default=medium)
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
                    'sf.sales_content_library') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

