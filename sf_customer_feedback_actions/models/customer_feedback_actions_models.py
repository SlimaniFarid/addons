# -*- coding: utf-8 -*-
"""Customer Feedback Action Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFeedbackAction(models.Model):
    _name = 'sf.feedback.action'
    _description = 'Feedback Action'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    feedback_summary = fields.Text(string='Feedback Summary', required=True)
    source = fields.Selection([
        ('survey', 'Survey'),
        ('meeting', 'Meeting'),
        ('complaint', 'Complaint'),
        ('review', 'Review'),
        ], string='Source', required=True, default=meeting)
    action = fields.Text(string='Action Committed', required=True)
    owner_id = fields.Many2one('res.users', string='Owner')
    due_date = fields.Date(string='Due Date')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('customer_validated', 'Customer Validated'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.feedback.action') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_customer_validated(self):
        self.write({'state': 'customer_validated'})

