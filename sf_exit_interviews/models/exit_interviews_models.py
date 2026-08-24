# -*- coding: utf-8 -*-
"""Exit Interview Records models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfExitInterview(models.Model):
    _name = 'sf.exit.interview'
    _description = 'Exit Interview'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Leaving Employee', required=True)
    leaving_date = fields.Date(string='Leaving Date', required=True)
    primary_reason = fields.Selection([
        ('salary', 'Salary'),
        ('management', 'Management'),
        ('career', 'Career Growth'),
        ('environment', 'Work Environment'),
        ('relocation', 'Relocation'),
        ('other', 'Other'),
        ], string='Primary Reason', required=True)
    would_return = fields.Boolean(string='Would Return')
    feedback = fields.Html(string='Feedback')
    actions = fields.Text(string='Improvement Actions')
    interviewer_id = fields.Many2one('res.users', string='Interviewer')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('shared', 'Shared with HR'),
        ], string='Status', default='scheduled', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.exit.interview') or 'NEW'
        return super().create(vals_list)

    def action_done(self):
        self.write({'state': 'done'})

    def action_shared(self):
        self.write({'state': 'shared'})

