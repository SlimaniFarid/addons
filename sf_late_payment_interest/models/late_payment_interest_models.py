# -*- coding: utf-8 -*-
"""Late Payment Interest Calculator models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLateInterest(models.Model):
    _name = 'sf.late.interest'
    _description = 'Late Interest Run'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rate_percent = fields.Float(string='Annual Rate %', default=5.0)
    grace_days = fields.Integer(string='Grace Days', default=30)
    as_of_date = fields.Date(string='As Of', default=fields.Date.today)
    total_interest = fields.Float(string='Total Interest')
    invoice_count = fields.Integer(string='Overdue Invoices')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Computed'),
        ('invoiced', 'Invoiced'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.late.interest') or 'NEW'
        return super().create(vals_list)

    def action_computed(self):
        self.write({'state': 'computed'})

    def action_invoiced(self):
        self.write({'state': 'invoiced'})

