# -*- coding: utf-8 -*-
"""Sales Territory Planner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_territory_planner(models.Model):
    _name = 'sf.sales_territory_planner'
    _description = 'Sales Territory Planner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    territory_name = fields.Char(string='Territory', required=True)
    rep_id = fields.Many2one('res.users', string='Sales Rep', required=True)
    account_count = fields.Integer(string='Account Count')
    revenue_potential = fields.Monetary(string='Revenue Potential')
    workload_score = fields.Float(string='Workload Score')
    balance_note = fields.Text(string='Balance Notes')
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
                    'sf.sales_territory_planner') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

