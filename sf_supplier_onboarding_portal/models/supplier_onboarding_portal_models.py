# -*- coding: utf-8 -*-
"""Supplier Onboarding Portal Config models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_onboarding_portal(models.Model):
    _name = 'sf.supplier_onboarding_portal'
    _description = 'Supplier Onboarding Portal Config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    onboarding_step = fields.Char(string='Step', required=True)
    step_type = fields.Selection([
        ('document', 'Document'),
        ('form', 'Form'),
        ('approval', 'Approval'),
        ('training', 'Training'),
        ], string='Type', required=True)
    completed = fields.Boolean(string='Completed')
    notes = fields.Text(string='Notes')
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
                    'sf.supplier_onboarding_portal') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

