# -*- coding: utf-8 -*-
"""Data Quality Check Runner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfData_quality_check(models.Model):
    _name = 'sf.data_quality_check'
    _description = 'Data Quality Check Runner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    check_name = fields.Char(string='Check Name', required=True)
    model_checked = fields.Char(string='Model Checked', required=True)
    completeness_percent = fields.Float(string='Completeness %')
    accuracy_percent = fields.Float(string='Accuracy %')
    issues_found = fields.Integer(string='Issues Found')
    remediation = fields.Text(string='Remediation')
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
                    'sf.data_quality_check') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

