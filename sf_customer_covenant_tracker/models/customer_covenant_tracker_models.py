# -*- coding: utf-8 -*-
"""Customer Contract Covenant Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_covenant_tracker(models.Model):
    _name = 'sf.customer_covenant_tracker'
    _description = 'Customer Contract Covenant Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    covenant_type = fields.Selection([
        ('min_purchase', 'Minimum Purchase'),
        ('exclusivity', 'Exclusivity'),
        ('volume_target', 'Volume Target'),
        ], string='Type', required=True)
    threshold = fields.Float(string='Threshold')
    actual = fields.Float(string='Actual')
    compliant = fields.Boolean(string='Compliant')
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
                    'sf.customer_covenant_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

