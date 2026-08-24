# -*- coding: utf-8 -*-
"""Customer Document Vault models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomerDoc(models.Model):
    _name = 'sf.customer.doc'
    _description = 'Customer Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    doc_type = fields.Selection([
        ('contract', 'Signed Contract'),
        ('insurance', 'Insurance Certificate'),
        ('audit', 'Audit Report'),
        ('compliance', 'Compliance Cert'),
        ('other', 'Other'),
        ], string='Document Type', required=True)
    received_date = fields.Date(string='Received')
    expiry_date = fields.Date(string='Expiry')
    attachment_ids = fields.Char(string='Files')
    chase_date = fields.Date(string='Chase Date')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('missing', 'Missing'),
        ('received', 'Received'),
        ('expired', 'Expired'),
        ], string='Status', default='missing', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.doc') or 'NEW'
        return super().create(vals_list)

    def action_received(self):
        self.write({'state': 'received'})

    def action_expired(self):
        self.write({'state': 'expired'})

