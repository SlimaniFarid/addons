# -*- coding: utf-8 -*-
"""Risk Mitigation Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_risk_mitigation_plan2(models.Model):
    _name = 'sf.supplier_risk_mitigation_plan2'
    _description = 'Risk Mitigation Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    risk_desc = fields.Text(string='Risk', required=True)
    mitigation_type = fields.Selection([
        ('dual_sourcing', 'Dual Sourcing'),
        ('buffer_stock', 'Buffer Stock'),
        ('contract', 'Contract Clause'),
        ('exit_plan', 'Exit Plan'),
        ], string='Type', required=True)
    implementation_date = fields.Date(string='Implementation')
    status_note = fields.Text(string='Status')
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
                    'sf.supplier_risk_mitigation_plan2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

