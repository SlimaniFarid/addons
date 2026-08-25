# -*- coding: utf-8 -*-
"""Third-Party Risk Assessment models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfThird_party_risk(models.Model):
    _name = 'sf.third_party_risk'
    _description = 'Third-Party Risk Assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Third Party', required=True)
    data_access = fields.Selection([
        ('none', 'None'),
        ('limited', 'Limited'),
        ('sensitive', 'Sensitive'),
        ('critical', 'Critical'),
        ], string='Data Access', required=True)
    criticality = fields.Selection([
        ('critical', 'Critical'),
        ('important', 'Important'),
        ('standard', 'Standard'),
        ], string='Criticality', default=standard)
    risk_score = fields.Integer(string='Risk Score (1-25)')
    mitigation = fields.Text(string='Mitigation Plan')
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
                    'sf.third_party_risk') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

