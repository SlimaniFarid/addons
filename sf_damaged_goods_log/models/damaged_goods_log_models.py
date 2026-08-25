# -*- coding: utf-8 -*-
"""Damaged Goods Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDamagedGoods(models.Model):
    _name = 'sf.damaged.goods'
    _description = 'Damaged Goods Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity')
    cause = fields.Selection([
        ('handling', 'Handling'),
        ('carrier', 'Carrier'),
        ('storage', 'Storage Conditions'),
        ('other', 'Other'),
        ], string='Cause', required=True)
    responsible = fields.Selection([
        ('internal', 'Internal'),
        ('carrier', 'Carrier'),
        ('customer', 'Customer'),
        ('unknown', 'Unknown'),
        ], string='Responsible', default=internal)
    estimated_cost = fields.Monetary(string='Estimated Cost')
    recovered = fields.Boolean(string='Cost Recovered')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('investigated', 'Investigated'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.damaged.goods') or 'NEW'
        return super().create(vals_list)

    def action_investigated(self):
        self.write({'state': 'investigated'})

    def action_closed(self):
        self.write({'state': 'closed'})

