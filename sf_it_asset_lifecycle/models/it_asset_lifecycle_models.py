# -*- coding: utf-8 -*-
"""IT Asset Lifecycle Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfIt_asset_lifecycle(models.Model):
    _name = 'sf.it_asset_lifecycle'
    _description = 'IT Asset Lifecycle Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    asset_tag = fields.Char(string='Asset Tag', required=True)
    asset_type = fields.Selection([
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('monitor', 'Monitor'),
        ('phone', 'Phone'),
        ('server', 'Server'),
        ], string='Type', required=True)
    assigned_to_id = fields.Many2one('hr.employee', string='Assigned To')
    purchase_date = fields.Date(string='Purchase Date')
    warranty_expiry = fields.Date(string='Warranty Expiry')
    refresh_due = fields.Date(string='Refresh Due')
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
                    'sf.it_asset_lifecycle') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

