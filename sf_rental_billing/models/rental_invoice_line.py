# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RentalInvoiceLine(models.Model):
    _name = 'sf.rental.billing.rental.invoice.line'
    _description = 'Rental Invoice Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    contract_id = fields.Many2one(required=True, comodel_name='rental.contract', ondelete='cascade')
    period_start = fields.Date(string='Period Start')
    period_end = fields.Date(string='Period End')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')

