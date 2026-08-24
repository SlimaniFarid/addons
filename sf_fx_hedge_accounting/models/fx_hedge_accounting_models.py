# -*- coding: utf-8 -*-
"""FX Hedge Accounting (IFRS 9) models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFx_hedge_accounting(models.Model):
    _name = 'sf.fx_hedge_accounting'
    _description = 'FX Hedge Accounting (IFRS 9)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    hedge_id = fields.Many2one('sf.fx.hedge', string='Hedge')
    designation = fields.Selection([
        ('cash_flow', 'Cash Flow Hedge'),
        ('fair_value', 'Fair Value Hedge'),
        ], string='Designation', required=True)
    effectiveness_percent = fields.Float(string='Effectiveness %')
    reclass_date = fields.Date(string='Reclassification Date')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.fx_hedge_accounting') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

