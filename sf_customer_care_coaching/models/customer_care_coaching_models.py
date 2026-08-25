# -*- coding: utf-8 -*-
"""Customer Care Coaching Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_coaching(models.Model):
    _name = 'sf.customer_care_coaching'
    _description = 'Customer Care Coaching Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Agent', required=True)
    coach_id = fields.Many2one('res.users', string='Coach')
    coaching_date = fields.Date(string='Date', default=fields.Date.today)
    quality_review = fields.Html(string='Quality Review')
    improvement_areas = fields.Text(string='Improvement Areas')
    next_review = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer_care_coaching') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

