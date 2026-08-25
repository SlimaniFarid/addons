# -*- coding: utf-8 -*-
"""Supplier Risk Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierRisk(models.Model):
    _name = 'sf.supplier.risk'
    _description = 'Supplier Risk'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    risk_type = fields.Selection([
        ('financial', 'Financial'),
        ('geo', 'Geographic'),
        ('single_source', 'Single Source'),
        ('compliance', 'Compliance'),
        ('capacity', 'Capacity'),
        ], string='Risk Type', required=True)
    score = fields.Integer(string='Risk Score (1-25)')
    mitigation = fields.Text(string='Mitigation Plan')
    contingency = fields.Text(string='Contingency (Backup Source)')
    review_date = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('identified', 'Identified'),
        ('mitigating', 'Mitigating'),
        ('closed', 'Closed'),
        ], string='Status', default='identified', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.risk') or 'NEW'
        return super().create(vals_list)

    def action_mitigating(self):
        self.write({'state': 'mitigating'})

    def action_closed(self):
        self.write({'state': 'closed'})

