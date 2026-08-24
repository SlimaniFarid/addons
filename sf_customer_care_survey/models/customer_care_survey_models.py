# -*- coding: utf-8 -*-
"""Customer Care Survey Runner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_survey(models.Model):
    _name = 'sf.customer_care_survey'
    _description = 'Customer Care Survey Runner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    survey_name = fields.Char(string='Survey Name', required=True)
    survey_type = fields.Selection([
        ('nps', 'NPS'),
        ('csat', 'CSAT'),
        ('ces', 'Customer Effort Score'),
        ], string='Type', required=True)
    sent_count = fields.Integer(string='Sent')
    response_count = fields.Integer(string='Responses')
    avg_score = fields.Float(string='Average Score')
    action_plan = fields.Text(string='Action Plan')
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
                    'sf.customer_care_survey') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

