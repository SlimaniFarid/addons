# -*- coding: utf-8 -*-
"""Key Account Plans (JBP) models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAccountPlan(models.Model):
    _name = 'sf.account.plan'
    _description = 'Key Account Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Key Account', required=True)
    plan_year = fields.Integer(string='Plan Year')
    objectives = fields.Html(string='Objectives')
    joint_actions = fields.Html(string='Joint Actions')
    revenue_target = fields.Monetary(string='Revenue Target')
    review_date = fields.Date(string='Next Review')
    owner_id = fields.Many2one('res.users', string='Plan Owner')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('review', 'In Review'),
        ('closed', 'Closed'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.account.plan') or 'NEW'
        return super().create(vals_list)

    def action_active(self):
        self.write({'state': 'active'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_closed(self):
        self.write({'state': 'closed'})

