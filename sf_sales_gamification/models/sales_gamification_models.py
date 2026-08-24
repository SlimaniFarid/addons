# -*- coding: utf-8 -*-
"""Sales Gamification Rules models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_gamification(models.Model):
    _name = 'sf.sales_gamification'
    _description = 'Sales Gamification Rules'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    challenge_name = fields.Char(string='Challenge', required=True)
    metric = fields.Selection([
        ('revenue', 'Revenue'),
        ('calls', 'Calls'),
        ('meetings', 'Meetings'),
        ('deals', 'Deals Closed'),
        ], string='Metric', required=True)
    target = fields.Float(string='Target')
    reward = fields.Char(string='Reward')
    start_date = fields.Date(string='Start')
    end_date = fields.Date(string='End')
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
                    'sf.sales_gamification') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

