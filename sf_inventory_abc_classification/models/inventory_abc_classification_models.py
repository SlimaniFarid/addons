# -*- coding: utf-8 -*-
"""Inventory ABC Classification models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfInventory_abc_classification(models.Model):
    _name = 'sf.inventory_abc_classification'
    _description = 'Inventory ABC Classification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    annual_value = fields.Monetary(string='Annual Value')
    movement_class = fields.Selection([
        ('fast', 'Fast'),
        ('medium', 'Medium'),
        ('slow', 'Slow'),
        ('dead', 'Dead'),
        ], string='Movement', required=True)
    abc_class = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ], string='ABC Class')
    count_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
        ], string='Count Frequency', default=quarterly)
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
                    'sf.inventory_abc_classification') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

