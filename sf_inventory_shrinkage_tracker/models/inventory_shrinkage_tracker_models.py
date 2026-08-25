# -*- coding: utf-8 -*-
"""Inventory Shrinkage Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfInventory_shrinkage_tracker(models.Model):
    _name = 'sf.inventory_shrinkage_tracker'
    _description = 'Inventory Shrinkage Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period = fields.Char(string='Period', required=True)
    shrinkage_type = fields.Selection([
        ('theft', 'Theft'),
        ('damage', 'Damage'),
        ('admin_error', 'Admin Error'),
        ('supplier_fraud', 'Supplier Fraud'),
        ], string='Type', required=True)
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity Lost')
    cost = fields.Monetary(string='Cost Impact')
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
                    'sf.inventory_shrinkage_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

