# -*- coding: utf-8 -*-
"""Carrier Performance Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCarrierPerf(models.Model):
    _name = 'sf.carrier.perf'
    _description = 'Carrier Performance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    carrier_id = fields.Many2one('res.partner', string='Carrier', required=True)
    period_month = fields.Date(string='Period', required=True)
    shipments = fields.Integer(string='Shipments')
    on_time = fields.Integer(string='On-Time')
    damaged = fields.Integer(string='Damaged')
    claims_amount = fields.Monetary(string='Claims Amount')
    otd_percent = fields.Float(string='On-Time %')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.carrier.perf') or 'NEW'
        return super().create(vals_list)

    def action_validated(self):
        self.write({'state': 'validated'})

