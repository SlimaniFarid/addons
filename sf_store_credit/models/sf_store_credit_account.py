# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfStoreCreditAccount(models.Model):
    _name = 'sf.store.credit.account'
    _description = 'Store Credit Account'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.store.credit.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True,
                                 ondelete='restrict')
    balance = fields.Monetary(string='Available Balance', currency_field='currency_id',
                              compute='_compute_balance', store=True)
    credit_ids = fields.One2many('sf.store.credit', 'account_id', string='Credits')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('partner_company_uniq', 'unique(partner_id, company_id)',
         'An account already exists for this customer and company.'),
    ]

    @api.depends('credit_ids.state', 'credit_ids.remaining')
    def _compute_balance(self):
        for account in self:
            credits = account.credit_ids.filtered(
                lambda c: c.state in ('confirmed', 'used', 'adjusted'))
            account.balance = sum(credits.mapped('remaining'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.store.credit.account')
        return super().create(vals_list)