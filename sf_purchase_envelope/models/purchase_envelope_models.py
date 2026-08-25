# -*- coding: utf-8 -*-
"""Category Purchase Envelopes models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPurchaseEnvelope(models.Model):
    _name = 'sf.purchase.envelope'
    _description = 'Purchase Envelope'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    category_name = fields.Char(string='Category', required=True)
    fiscal_year = fields.Integer(string='Fiscal Year')
    envelope_amount = fields.Monetary(string='Envelope', required=True)
    committed = fields.Monetary(string='Committed')
    consumed = fields.Monetary(string='Consumed')
    owner_id = fields.Many2one('res.users', string='Category Owner')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.purchase.envelope') or 'NEW'
        return super().create(vals_list)

    def action_closed(self):
        self.write({'state': 'closed'})

