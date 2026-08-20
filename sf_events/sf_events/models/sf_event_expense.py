# -*- coding: utf-8 -*-
from odoo import fields, models


class SfEventExpense(models.Model):
    _name = 'sf.event.expense'
    _description = 'Event Expense'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.events.activity.mixin']
    _order = 'expense_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    event_id = fields.Many2one('sf.event', string='Event', required=True, ondelete='cascade')
    category = fields.Selection([
        ('venue', 'Venue'),
        ('catering', 'Catering'),
        ('speaker', 'Speaker'),
        ('marketing', 'Marketing'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ], string='Category', default='other')
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    vendor_partner_id = fields.Many2one('res.partner', string='Vendor', ondelete='set null')
    expense_date = fields.Date(string='Expense Date', default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.event.expense')
        return super().create(vals_list)