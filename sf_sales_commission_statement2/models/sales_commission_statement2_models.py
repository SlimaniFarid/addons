# -*- coding: utf-8 -*-
"""Commission Statement models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_commission_statement2(models.Model):
    _name = 'sf.sales_commission_statement2'
    _description = 'Commission Statement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rep_id = fields.Many2one('res.users', string='Sales Rep', required=True)
    period = fields.Char(string='Period', required=True)
    total_sales = fields.Monetary(string='Total Sales')
    commission_rate = fields.Float(string='Rate %')
    gross_commission = fields.Monetary(string='Gross')
    deductions = fields.Monetary(string='Deductions')
    net_commission = fields.Monetary(string='Net')
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
                    'sf.sales_commission_statement2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

