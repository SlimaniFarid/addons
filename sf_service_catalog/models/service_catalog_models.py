# -*- coding: utf-8 -*-
"""Internal Service Catalog models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfServiceItem(models.Model):
    _name = 'sf.service.item'
    _description = 'Service Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    service_name = fields.Char(string='Service', required=True)
    description = fields.Html(string='Description')
    target_sla_hours = fields.Float(string='Target SLA (h)')
    owner_id = fields.Many2one('res.users', string='Service Owner')
    request_types = fields.Text(string='Request Types')
    active = fields.Boolean(string='Active', default=True)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('retired', 'Retired'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.service.item') or 'NEW'
        return super().create(vals_list)

    def action_published(self):
        self.write({'state': 'published'})

    def action_retired(self):
        self.write({'state': 'retired'})

