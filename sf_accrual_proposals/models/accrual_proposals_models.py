# -*- coding: utf-8 -*-
"""Month-End Accrual Proposals models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAccrual(models.Model):
    _name = 'sf.accrual'
    _description = 'Accrual'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    label = fields.Char(string='Label', required=True)
    period_month = fields.Date(string='Period', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    reversal_month = fields.Date(string='Reversal Month')
    category = fields.Selection([
        ('expense', 'Expense Accrual'),
        ('revenue', 'Revenue Accrual'),
        ('other', 'Other'),
        ], string='Category')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('proposed', 'Proposed'),
        ('approved', 'Approved'),
        ('posted', 'Posted'),
        ('reversed', 'Reversed'),
        ], string='Status', default='proposed', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.accrual') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_posted(self):
        self.write({'state': 'posted'})

    def action_reversed(self):
        self.write({'state': 'reversed'})

