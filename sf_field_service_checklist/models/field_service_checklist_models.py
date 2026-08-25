# -*- coding: utf-8 -*-
"""Field Service Checklist models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfField_service_checklist(models.Model):
    _name = 'sf.field_service_checklist'
    _description = 'Field Service Checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    service_order_ref = fields.Char(string='Service Order', required=True)
    checklist_type = fields.Selection([
        ('pre_work', 'Pre-Work'),
        ('task', 'Task List'),
        ('post_work', 'Post-Work'),
        ('safety', 'Safety Check'),
        ], string='Type', required=True)
    items = fields.Html(string='Checklist Items')
    customer_signature = fields.Boolean(string='Customer Signed')
    technician_id = fields.Many2one('res.users', string='Technician')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.field_service_checklist') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

