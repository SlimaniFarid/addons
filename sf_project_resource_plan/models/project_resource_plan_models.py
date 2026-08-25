# -*- coding: utf-8 -*-
"""Resource Allocation Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProject_resource_plan(models.Model):
    _name = 'sf.project_resource_plan'
    _description = 'Resource Allocation Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Resource', required=True)
    project_name = fields.Char(string='Project', required=True)
    allocation_percent = fields.Float(string='Allocation %')
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To')
    notes = fields.Text(string='Notes')
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
                    'sf.project_resource_plan') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

