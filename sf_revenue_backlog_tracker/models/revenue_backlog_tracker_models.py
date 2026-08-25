# -*- coding: utf-8 -*-
"""Revenue Backlog Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRevenueBacklog(models.Model):
    _name = 'sf.revenue.backlog'
    _description = 'Backlog Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    contract_ref = fields.Char(string='Contract / Order Ref', required=True)
    backlog_amount = fields.Monetary(string='Backlog Amount', required=True)
    expected_invoice_month = fields.Date(string='Expected Invoice Month')
    invoiced_amount = fields.Float(string='Invoiced So Far')
    risk_note = fields.Text(string='Risk Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('partially_invoiced', 'Partially Invoiced'),
        ('invoiced', 'Invoiced'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.revenue.backlog') or 'NEW'
        return super().create(vals_list)

    def action_partially_invoiced(self):
        self.write({'state': 'partially_invoiced'})

    def action_invoiced(self):
        self.write({'state': 'invoiced'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

