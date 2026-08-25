# -*- coding: utf-8 -*-
"""Invoice Matching Rules models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_invoice_3way_match3(models.Model):
    _name = 'sf.supplier_invoice_3way_match3'
    _description = 'Invoice Matching Rules'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rule_name = fields.Char(string='Rule Name', required=True)
    match_field = fields.Selection([
        ('amount', 'Amount'),
        ('reference', 'Reference'),
        ('date', 'Date'),
        ('partner', 'Partner'),
        ], string='Match Field', required=True)
    tolerance_percent = fields.Float(string='Tolerance %', default=2.0)
    auto_match = fields.Boolean(string='Auto-Match', default=True)
    priority = fields.Integer(string='Priority', default=10)
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
                    'sf.supplier_invoice_3way_match3') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

