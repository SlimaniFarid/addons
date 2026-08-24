# -*- coding: utf-8 -*-
"""Software License Renewal Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLicenseSub(models.Model):
    _name = 'sf.license.sub'
    _description = 'License Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    software = fields.Char(string='Software', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    seats = fields.Integer(string='Seats', default=1)
    annual_cost = fields.Monetary(string='Annual Cost')
    renewal_date = fields.Date(string='Renewal Date', required=True)
    auto_renew = fields.Boolean(string='Auto-Renewal')
    owner_id = fields.Many2one('res.users', string='Owner')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('renewal_due', 'Renewal Due'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.license.sub') or 'NEW'
        return super().create(vals_list)

    def action_renewal_due(self):
        self.write({'state': 'renewal_due'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

