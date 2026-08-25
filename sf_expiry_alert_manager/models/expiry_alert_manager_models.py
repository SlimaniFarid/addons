# -*- coding: utf-8 -*-
"""Expiry & FEFO Alert Manager models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfExpiryAlert(models.Model):
    _name = 'sf.expiry.alert'
    _description = 'Expiry Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    lot_id = fields.Many2one('stock.lot', string='Lot', required=True)
    product_id = fields.Many2one('product.product', string='Product')
    expiry_date = fields.Date(string='Expiry Date', required=True)
    alert_days = fields.Integer(string='Alert Before (days)', default=30)
    quantity = fields.Float(string='Quantity')
    disposition = fields.Selection([
        ('sell', 'Sell First (FEFO)'),
        ('discount', 'Discount'),
        ('write_off', 'Write Off'),
        ('donate', 'Donate'),
        ], string='Disposition', default=sell)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('actioned', 'Actioned'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.expiry.alert') or 'NEW'
        return super().create(vals_list)

    def action_actioned(self):
        self.write({'state': 'actioned'})

    def action_closed(self):
        self.write({'state': 'closed'})

