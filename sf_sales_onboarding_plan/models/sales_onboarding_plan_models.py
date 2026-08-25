# -*- coding: utf-8 -*-
"""Sales Onboarding Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_onboarding_plan(models.Model):
    _name = 'sf.sales_onboarding_plan'
    _description = 'Sales Onboarding Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rep_id = fields.Many2one('res.users', string='New Rep', required=True)
    onboarding_step = fields.Char(string='Step', required=True)
    step_type = fields.Selection([
        ('product', 'Product Training'),
        ('shadow', 'Shadow Call'),
        ('certification', 'Certification'),
        ('first_deal', 'First Deal'),
        ], string='Type', required=True)
    completed = fields.Boolean(string='Completed')
    target_date = fields.Date(string='Target Date')
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
                    'sf.sales_onboarding_plan') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

