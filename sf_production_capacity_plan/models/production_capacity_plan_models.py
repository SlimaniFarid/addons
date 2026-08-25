# -*- coding: utf-8 -*-
"""Production Capacity Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_capacity_plan(models.Model):
    _name = 'sf.production_capacity_plan'
    _description = 'Production Capacity Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center', required=True)
    period = fields.Char(string='Period', required=True)
    available_hours = fields.Float(string='Available Hours')
    planned_hours = fields.Float(string='Planned Load')
    utilization_percent = fields.Float(string='Utilization %')
    overtime_needed = fields.Float(string='Overtime Needed (h)')
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
                    'sf.production_capacity_plan') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

