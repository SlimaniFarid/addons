# -*- coding: utf-8 -*-
"""Peak Season Planning models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPeakPlan(models.Model):
    _name = 'sf.peak.plan'
    _description = 'Peak Season Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    season = fields.Selection([
        ('q4', 'Q4 Peak'),
        ('summer', 'Summer'),
        ('campaign', 'Campaign'),
        ('other', 'Other'),
        ], string='Season', required=True)
    start_date = fields.Date(string='Season Start', required=True)
    temp_staff = fields.Integer(string='Temporary Staff')
    stock_build_target = fields.Float(string='Stock Build Target')
    carrier_capacity_booked = fields.Boolean(string='Carrier Capacity Booked')
    daily_ship_target = fields.Integer(string='Daily Ship Target')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planning', 'Planning'),
        ('ready', 'Ready'),
        ('in_season', 'In Season'),
        ('reviewed', 'Reviewed'),
        ], string='Status', default='planning', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.peak.plan') or 'NEW'
        return super().create(vals_list)

    def action_ready(self):
        self.write({'state': 'ready'})

    def action_in_season(self):
        self.write({'state': 'in_season'})

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

