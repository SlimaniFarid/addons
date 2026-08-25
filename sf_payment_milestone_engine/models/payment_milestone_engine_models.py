# -*- coding: utf-8 -*-
"""Payment Milestone Engine models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPaymentMilestone(models.Model):
    _name = 'sf.payment.milestone'
    _description = 'Payment Milestone Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    milestone_no = fields.Integer(string='Milestone #', default=1)
    percent = fields.Float(string='% of Total')
    due_date = fields.Date(string='Due Date')
    amount = fields.Monetary(string='Amount')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.payment.milestone') or 'NEW'
        return super().create(vals_list)


