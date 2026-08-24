# -*- coding: utf-8 -*-
"""Contract Renewal Pipeline models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_contract_renewal_pipeline(models.Model):
    _name = 'sf.customer_contract_renewal_pipeline'
    _description = 'Contract Renewal Pipeline'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    contract_ref = fields.Char(string='Contract', required=True)
    expiry_date = fields.Date(string='Expiry', required=True)
    renewal_probability = fields.Float(string='Renewal Probability %')
    revenue_value = fields.Monetary(string='Revenue Value')
    owner_id = fields.Many2one('res.users', string='Owner')
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
                    'sf.customer_contract_renewal_pipeline') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

