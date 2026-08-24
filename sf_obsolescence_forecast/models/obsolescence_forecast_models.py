# -*- coding: utf-8 -*-
"""Obsolescence Forecast Model models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfObsolescence_forecast(models.Model):
    _name = 'sf.obsolescence_forecast'
    _description = 'Obsolescence Forecast Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    movement_trend = fields.Selection([
        ('growing', 'Growing'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
        ('dead', 'Dead'),
        ], string='Trend', required=True)
    lifecycle_stage = fields.Selection([
        ('introduction', 'Introduction'),
        ('growth', 'Growth'),
        ('maturity', 'Maturity'),
        ('decline', 'Decline'),
        ], string='Lifecycle', default=maturity)
    risk_score = fields.Integer(string='Risk Score (0-100)')
    recommended_action = fields.Text(string='Recommended Action')
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
                    'sf.obsolescence_forecast') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

