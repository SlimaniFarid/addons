# -*- coding: utf-8 -*-
"""Invoice Discounting & Factoring Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDiscountedInvoice(models.Model):
    _name = 'sf.discounted.invoice'
    _description = 'Discounted Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    factor_id = fields.Many2one('res.partner', string='Factor / Bank', required=True)
    invoice_ref = fields.Char(string='Invoice Ref', required=True)
    face_amount = fields.Monetary(string='Face Amount', required=True)
    advance_percent = fields.Float(string='Advance %', default=80.0)
    fee_percent = fields.Float(string='Fee %')
    maturity_date = fields.Date(string='Maturity')
    settled = fields.Boolean(string='Settled')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('registered', 'Registered'),
        ('funded', 'Funded'),
        ('settled', 'Settled'),
        ], string='Status', default='registered', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.discounted.invoice') or 'NEW'
        return super().create(vals_list)

    def action_funded(self):
        self.write({'state': 'funded'})

    def action_settled(self):
        self.write({'state': 'settled'})

