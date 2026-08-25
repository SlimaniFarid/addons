# -*- coding: utf-8 -*-
"""Sales Battle Rhythm Planner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_battle_rhythm(models.Model):
    _name = 'sf.sales_battle_rhythm'
    _description = 'Sales Battle Rhythm Planner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    week_label = fields.Char(string='Week', required=True)
    monday_pipeline_done = fields.Boolean(string='Monday Pipeline Review')
    wednesday_coaching_done = fields.Boolean(string='Wednesday Coaching')
    friday_forecast_done = fields.Boolean(string='Friday Forecast')
    blockers = fields.Text(string='Blockers')
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
                    'sf.sales_battle_rhythm') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

