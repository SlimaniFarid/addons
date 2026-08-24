# -*- coding: utf-8 -*-
"""Production Schedule Variance Alert models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_schedule_alert(models.Model):
    _name = 'sf.production_schedule_alert'
    _description = 'Production Schedule Variance Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order', required=True)
    planned_start = fields.Date(string='Planned Start')
    actual_start = fields.Date(string='Actual Start')
    variance_days = fields.Integer(string='Variance (days)')
    root_cause = fields.Selection([
        ('material', 'Material Shortage'),
        ('machine', 'Machine Downtime'),
        ('labor', 'Labor Shortage'),
        ('priority', 'Priority Change'),
        ], string='Root Cause')
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
                    'sf.production_schedule_alert') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

