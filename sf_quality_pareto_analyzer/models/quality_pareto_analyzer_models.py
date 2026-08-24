# -*- coding: utf-8 -*-
"""Quality Pareto Analyzer models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_pareto_analyzer(models.Model):
    _name = 'sf.quality_pareto_analyzer'
    _description = 'Quality Pareto Analyzer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    defect_type = fields.Char(string='Defect Type', required=True)
    occurrences = fields.Integer(string='Occurrences', required=True)
    cost = fields.Monetary(string='Total Cost')
    cumulative_percent = fields.Float(string='Cumulative %')
    priority = fields.Selection([
        ('critical', 'Critical'),
        ('important', 'Important'),
        ('minor', 'Minor'),
        ], string='Priority', default=minor)
    action_ref = fields.Char(string='Improvement Action')
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
                    'sf.quality_pareto_analyzer') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

