# -*- coding: utf-8 -*-
"""Pipeline Review Meeting Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_pipeline_review(models.Model):
    _name = 'sf.sales_pipeline_review'
    _description = 'Pipeline Review Meeting Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    review_date = fields.Date(string='Review Date', required=True, default=fields.Date.today)
    rep_id = fields.Many2one('res.users', string='Sales Rep', required=True)
    stage_movements = fields.Html(string='Stage Movements')
    stuck_deals = fields.Text(string='Stuck Deals')
    forecast_change = fields.Monetary(string='Forecast Change')
    actions = fields.Text(string='Actions')
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
                    'sf.sales_pipeline_review') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

