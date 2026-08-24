# -*- coding: utf-8 -*-
"""Engagement Action Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEmployee_engagement_action(models.Model):
    _name = 'sf.employee_engagement_action'
    _description = 'Engagement Action Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    action = fields.Char(string='Action', required=True)
    source_survey = fields.Char(string='Source Survey')
    owner_id = fields.Many2one('res.users', string='Owner', required=True)
    due_date = fields.Date(string='Due Date')
    impact = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ], string='Expected Impact', default=medium)
    status_note = fields.Text(string='Status')
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
                    'sf.employee_engagement_action') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

