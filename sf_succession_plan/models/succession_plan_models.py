# -*- coding: utf-8 -*-
"""Succession Plan Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSuccession_plan(models.Model):
    _name = 'sf.succession_plan'
    _description = 'Succession Plan Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    position = fields.Char(string='Key Position', required=True)
    candidate_id = fields.Many2one('hr.employee', string='Successor Candidate')
    readiness = fields.Selection([
        ('ready_now', 'Ready Now'),
        ('1_year', 'Ready in 1 Year'),
        ('2_years', 'Ready in 2 Years'),
        ('3_years', '3+ Years'),
        ], string='Readiness', default='ready_now')
    development_actions = fields.Html(string='Development Actions')
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
                    'sf.succession_plan') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

