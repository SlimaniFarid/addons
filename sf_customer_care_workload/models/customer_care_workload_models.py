# -*- coding: utf-8 -*-
"""Care Workload Balancer models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_workload(models.Model):
    _name = 'sf.customer_care_workload'
    _description = 'Care Workload Balancer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    agent_id = fields.Many2one('res.users', string='Agent', required=True)
    period = fields.Char(string='Period', required=True)
    open_cases = fields.Integer(string='Open Cases')
    capacity_cases = fields.Integer(string='Capacity')
    overloaded = fields.Boolean(string='Overloaded')
    redistribution = fields.Text(string='Redistribution Notes')
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
                    'sf.customer_care_workload') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

