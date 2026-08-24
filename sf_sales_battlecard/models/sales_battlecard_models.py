# -*- coding: utf-8 -*-
"""Competitive Battle Cards models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_battlecard(models.Model):
    _name = 'sf.sales_battlecard'
    _description = 'Competitive Battle Cards'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    competitor = fields.Char(string='Competitor', required=True)
    their_strengths = fields.Html(string='Their Strengths')
    their_weaknesses = fields.Html(string='Their Weaknesses')
    win_strategy = fields.Html(string='Win Strategy')
    proof_points = fields.Html(string='Proof Points')
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
                    'sf.sales_battlecard') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

