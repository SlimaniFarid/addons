# -*- coding: utf-8 -*-
"""Customer Journey Stage Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_journey_stage(models.Model):
    _name = 'sf.customer_journey_stage'
    _description = 'Customer Journey Stage Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    stage = fields.Selection([
        ('awareness', 'Awareness'),
        ('consideration', 'Consideration'),
        ('decision', 'Decision'),
        ('retention', 'Retention'),
        ('advocacy', 'Advocacy'),
        ], string='Stage', required=True)
    touchpoints = fields.Integer(string='Touchpoints')
    days_in_stage = fields.Integer(string='Days in Stage')
    next_action = fields.Text(string='Next Action')
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
                    'sf.customer_journey_stage') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

