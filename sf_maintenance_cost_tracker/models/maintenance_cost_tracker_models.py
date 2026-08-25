# -*- coding: utf-8 -*-
"""Maintenance Cost Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMaintenance_cost_tracker(models.Model):
    _name = 'sf.maintenance_cost_tracker'
    _description = 'Maintenance Cost Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', required=True)
    period = fields.Char(string='Period', required=True)
    preventive_cost = fields.Monetary(string='Preventive Cost')
    corrective_cost = fields.Monetary(string='Corrective Cost')
    parts_cost = fields.Monetary(string='Parts Cost')
    total_cost = fields.Monetary(string='Total Cost')
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
                    'sf.maintenance_cost_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

