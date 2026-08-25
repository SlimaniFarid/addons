# -*- coding: utf-8 -*-
"""Revenue Milestone Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRevenue_milestone(models.Model):
    _name = 'sf.revenue_milestone'
    _description = 'Revenue Milestone Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    contract_ref = fields.Char(string='Contract', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    total_value = fields.Monetary(string='Contract Value')
    milestone_percent = fields.Float(string='% Complete')
    recognized_to_date = fields.Monetary(string='Recognized to Date')
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
                    'sf.revenue_milestone') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

