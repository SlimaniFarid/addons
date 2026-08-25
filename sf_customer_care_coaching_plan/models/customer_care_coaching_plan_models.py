# -*- coding: utf-8 -*-
"""Care Coaching Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_coaching_plan(models.Model):
    _name = 'sf.customer_care_coaching_plan'
    _description = 'Care Coaching Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    agent_id = fields.Many2one('res.users', string='Agent', required=True)
    coach_id = fields.Many2one('res.users', string='Coach')
    skills_assessment = fields.Html(string='Skills Assessment')
    development_areas = fields.Text(string='Development Areas')
    milestones = fields.Html(string='Coaching Milestones')
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
                    'sf.customer_care_coaching_plan') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

