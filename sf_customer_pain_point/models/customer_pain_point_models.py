# -*- coding: utf-8 -*-
"""Customer Pain Point Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_pain_point(models.Model):
    _name = 'sf.customer_pain_point'
    _description = 'Customer Pain Point Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    pain_point = fields.Text(string='Pain Point', required=True)
    severity = fields.Selection([
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('minor', 'Minor'),
        ], string='Severity', required=True)
    product_impact = fields.Text(string='Product Impact')
    resolution_status = fields.Selection([
        ('identified', 'Identified'),
        ('in_progress', 'Being Addressed'),
        ('resolved', 'Resolved'),
        ], string='Status', default=identified)
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
                    'sf.customer_pain_point') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

