# -*- coding: utf-8 -*-
"""Telework Policy Manager models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfTelework_policy(models.Model):
    _name = 'sf.telework_policy'
    _description = 'Telework Policy Manager'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    policy_name = fields.Char(string='Policy Name', required=True)
    max_days_week = fields.Integer(string='Max Days/Week', default=2)
    eligibility_rule = fields.Text(string='Eligibility Rule')
    active = fields.Boolean(string='Active', default=True)
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
                    'sf.telework_policy') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

