# -*- coding: utf-8 -*-
"""Customer Journey Mapper models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_journey_mapper(models.Model):
    _name = 'sf.customer_journey_mapper'
    _description = 'Customer Journey Mapper'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    journey_stage = fields.Selection([
        ('awareness', 'Awareness'),
        ('consideration', 'Consideration'),
        ('purchase', 'Purchase'),
        ('onboarding', 'Onboarding'),
        ('retention', 'Retention'),
        ('advocacy', 'Advocacy'),
        ], string='Stage', required=True)
    experience_score = fields.Float(string='Experience Score (1-10)')
    pain_points = fields.Text(string='Pain Points')
    improvement = fields.Text(string='Improvement Action')
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
                    'sf.customer_journey_mapper') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

