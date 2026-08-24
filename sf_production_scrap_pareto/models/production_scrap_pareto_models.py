# -*- coding: utf-8 -*-
"""Scrap Pareto Analyzer models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_scrap_pareto(models.Model):
    _name = 'sf.production_scrap_pareto'
    _description = 'Scrap Pareto Analyzer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period = fields.Char(string='Period', required=True)
    scrap_reason = fields.Char(string='Scrap Reason', required=True)
    quantity = fields.Float(string='Qty Scrapped')
    cost = fields.Monetary(string='Cost')
    cumulative_percent = fields.Float(string='Cumulative %')
    action_ref = fields.Char(string='Improvement Action')
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
                    'sf.production_scrap_pareto') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

