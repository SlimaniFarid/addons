# -*- coding: utf-8 -*-
"""Supplier Payment Optimization models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_payment_optimization(models.Model):
    _name = 'sf.supplier_payment_optimization'
    _description = 'Supplier Payment Optimization'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    standard_terms_days = fields.Integer(string='Standard Terms (days)')
    early_discount_percent = fields.Float(string='Early Payment Discount %')
    early_discount_days = fields.Integer(string='Discount if Paid Within (days)')
    annual_benefit = fields.Monetary(string='Annual Benefit')
    recommendation = fields.Text(string='Recommendation')
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
                    'sf.supplier_payment_optimization') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

