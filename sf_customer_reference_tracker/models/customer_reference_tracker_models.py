# -*- coding: utf-8 -*-
"""Customer Reference Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_reference_tracker(models.Model):
    _name = 'sf.customer_reference_tracker'
    _description = 'Customer Reference Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Reference Customer', required=True)
    use_case = fields.Char(string='Use Case', required=True)
    reference_contact = fields.Char(string='Reference Contact')
    available_for_calls = fields.Boolean(string='Available for Calls')
    times_used = fields.Integer(string='Times Used in Sales')
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
                    'sf.customer_reference_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

