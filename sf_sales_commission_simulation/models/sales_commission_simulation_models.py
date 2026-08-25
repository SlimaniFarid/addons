# -*- coding: utf-8 -*-
"""Sales Commission Simulator models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_commission_simulation(models.Model):
    _name = 'sf.sales_commission_simulation'
    _description = 'Sales Commission Simulator'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    sim_name = fields.Char(string='Simulation Name', required=True)
    plan_type = fields.Selection([
        ('flat', 'Flat %'),
        ('tiered', 'Tiered'),
        ('accelerator', 'With Accelerator'),
        ], string='Plan Type', required=True)
    base_rate = fields.Float(string='Base Rate %')
    target_revenue = fields.Monetary(string='Target Revenue')
    simulated_payout = fields.Monetary(string='Simulated Payout')
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
                    'sf.sales_commission_simulation') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

