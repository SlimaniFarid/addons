# -*- coding: utf-8 -*-
"""Vendor SLA Monitoring models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVendorSla(models.Model):
    _name = 'sf.vendor.sla'
    _description = 'Vendor SLA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    service = fields.Char(string='Service', required=True)
    response_target_h = fields.Float(string='Response Target (h)')
    resolution_target_h = fields.Float(string='Resolution Target (h)')
    last_breach_date = fields.Date(string='Last Breach')
    breach_count = fields.Integer(string='Breaches (12m)')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('breached', 'Breached'),
        ('suspended', 'Suspended'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.vendor.sla') or 'NEW'
        return super().create(vals_list)

    def action_breached(self):
        self.write({'state': 'breached'})

    def action_suspended(self):
        self.write({'state': 'suspended'})

