# -*- coding: utf-8 -*-
"""Supplier Bank Change Alert models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBankChange(models.Model):
    _name = 'sf.bank.change'
    _description = 'Bank Change Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    old_iban = fields.Char(string='Old IBAN (masked)')
    new_iban = fields.Char(string='New IBAN (masked)')
    verification_call_done = fields.Boolean(string='Callback Verification Done')
    verified_by_id = fields.Many2one('res.users', string='Verified By')
    documents = fields.Html(string='Supporting Documents')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('received', 'Received'),
        ('verified', 'Verified'),
        ('applied', 'Applied'),
        ('rejected', 'Rejected - Fraud Suspected'),
        ], string='Status', default='received', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.bank.change') or 'NEW'
        return super().create(vals_list)

    def action_verified(self):
        self.write({'state': 'verified'})

    def action_applied(self):
        self.write({'state': 'applied'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

