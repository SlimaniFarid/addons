# -*- coding: utf-8 -*-
"""Sales Target Cascade models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_target_cascade(models.Model):
    _name = 'sf.sales_target_cascade'
    _description = 'Sales Target Cascade'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rep_id = fields.Many2one('res.users', string='Sales Rep', required=True)
    fiscal_year = fields.Integer(string='Year', required=True)
    annual_target = fields.Monetary(string='Annual Target', required=True)
    q1_target = fields.Monetary(string='Q1')
    q2_target = fields.Monetary(string='Q2')
    q3_target = fields.Monetary(string='Q3')
    q4_target = fields.Monetary(string='Q4')
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
                    'sf.sales_target_cascade') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

