# -*- coding: utf-8 -*-
"""Pallet SSCC Label Generator models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPalletSscc(models.Model):
    _name = 'sf.pallet.sscc'
    _description = 'Pallet Label'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    picking_id = fields.Many2one('stock.picking', string='Delivery', required=True)
    sscc_code = fields.Char(string='SSCC Code', required=True)
    pallet_type = fields.Selection([
        ('eur', 'EUR 80x120'),
        ('half', 'Half 60x80'),
        ('other', 'Other'),
        ], string='Pallet Type', default=eur)
    gross_weight = fields.Float(string='Gross Weight (kg)')
    printed = fields.Boolean(string='Printed')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('printed', 'Printed'),
        ('shipped', 'Shipped'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.pallet.sscc') or 'NEW'
        return super().create(vals_list)

    def action_printed(self):
        self.write({'state': 'printed'})

    def action_shipped(self):
        self.write({'state': 'shipped'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.pallet.sscc'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
