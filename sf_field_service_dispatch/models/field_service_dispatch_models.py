# -*- coding: utf-8 -*-
"""Field Service Dispatch Board models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfField_service_dispatch(models.Model):
    _name = 'sf.field_service_dispatch'
    _description = 'Field Service Dispatch Board'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    technician_id = fields.Many2one('res.users', string='Technician', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    service_type = fields.Selection([
        ('repair', 'Repair'),
        ('installation', 'Installation'),
        ('maintenance', 'Maintenance'),
        ('inspection', 'Inspection'),
        ], string='Service Type', required=True)
    scheduled_at = fields.Datetime(string='Scheduled')
    sla_hours = fields.Float(string='SLA (hours)')
    status_note = fields.Text(string='Status Notes')
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
                    'sf.field_service_dispatch') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

