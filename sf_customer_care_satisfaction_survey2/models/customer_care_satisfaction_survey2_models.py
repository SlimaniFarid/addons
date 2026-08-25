# -*- coding: utf-8 -*-
"""Post-Resolution Survey models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_satisfaction_survey2(models.Model):
    _name = 'sf.customer_care_satisfaction_survey2'
    _description = 'Post-Resolution Survey'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    resolution_ref = fields.Char(string='Resolution Ref', required=True)
    csat_score = fields.Float(string='CSAT (1-5)')
    effort_score = fields.Float(string='Effort Score (1-7)')
    open_feedback = fields.Text(string='Open Feedback')
    follow_up = fields.Boolean(string='Follow-up Needed')
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
                    'sf.customer_care_satisfaction_survey2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

