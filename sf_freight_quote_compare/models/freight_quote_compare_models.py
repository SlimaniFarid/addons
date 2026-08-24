# -*- coding: utf-8 -*-
"""Freight Quote Comparison models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFreightQuote(models.Model):
    _name = 'sf.freight.quote'
    _description = 'Freight Quote Comparison'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    shipment_ref = fields.Char(string='Shipment', required=True)
    carrier_id = fields.Many2one('res.partner', string='Carrier', required=True)
    base_cost = fields.Monetary(string='Base Cost', required=True)
    surcharges = fields.Monetary(string='Surcharges')
    transit_days = fields.Integer(string='Transit (days)')
    total_cost = fields.Monetary(string='Total')
    awarded = fields.Boolean(string='Awarded')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('received', 'Received'),
        ('awarded', 'Awarded'),
        ('lost', 'Not Selected'),
        ], string='Status', default='received', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.freight.quote') or 'NEW'
        return super().create(vals_list)

    def action_awarded(self):
        self.write({'state': 'awarded'})

    def action_lost(self):
        self.write({'state': 'lost'})

