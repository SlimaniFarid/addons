# -*- coding: utf-8 -*-
"""Warranty Cost Analytics models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfWarrantyCost(models.Model):
    _name = 'sf.warranty.cost'
    _description = 'Warranty Cost Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    claim_date = fields.Date(string='Claim Date', required=True, default=fields.Date.today)
    internal_cost = fields.Monetary(string='Internal Cost')
    recovered_from_supplier = fields.Monetary(string='Recovered')
    quality_signal = fields.Text(string='Quality Signal')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('analyzed', 'Analyzed'),
        ('recovered', 'Recovered'),
        ('absorbed', 'Absorbed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.warranty.cost') or 'NEW'
        return super().create(vals_list)

    def action_analyzed(self):
        self.write({'state': 'analyzed'})

    def action_recovered(self):
        self.write({'state': 'recovered'})

    def action_absorbed(self):
        self.write({'state': 'absorbed'})

