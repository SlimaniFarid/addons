# -*- coding: utf-8 -*-
"""Production Capacity Review Meeting models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_capacity_review(models.Model):
    _name = 'sf.production_capacity_review'
    _description = 'Production Capacity Review Meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    review_date = fields.Date(string='Review Date', required=True, default=fields.Date.today)
    chair_id = fields.Many2one('res.users', string='Chair')
    bottlenecks = fields.Html(string='Bottlenecks Identified')
    actions = fields.Html(string='Action Items')
    capacity_changes = fields.Text(string='Capacity Changes Needed')
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
                    'sf.production_capacity_review') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

