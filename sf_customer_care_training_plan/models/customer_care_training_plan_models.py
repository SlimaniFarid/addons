# -*- coding: utf-8 -*-
"""Care Training Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_training_plan(models.Model):
    _name = 'sf.customer_care_training_plan'
    _description = 'Care Training Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    agent_id = fields.Many2one('res.users', string='Agent', required=True)
    module_name = fields.Char(string='Module', required=True)
    completed_date = fields.Date(string='Completed')
    score = fields.Float(string='Score')
    certified = fields.Boolean(string='Certified')
    refresher_due = fields.Date(string='Refresher Due')
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
                    'sf.customer_care_training_plan') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

