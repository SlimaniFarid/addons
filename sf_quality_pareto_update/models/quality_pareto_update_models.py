# -*- coding: utf-8 -*-
"""Non-Conformance Pareto Update models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_pareto_update(models.Model):
    _name = 'sf.quality_pareto_update'
    _description = 'Non-Conformance Pareto Update'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period = fields.Char(string='Period', required=True)
    nc_type = fields.Char(string='NC Type', required=True)
    count = fields.Integer(string='Count', required=True)
    cost_impact = fields.Monetary(string='Cost Impact')
    cumulative_percent = fields.Float(string='Cumulative %')
    action_owner_id = fields.Many2one('res.users', string='Action Owner')
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
                    'sf.quality_pareto_update') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

