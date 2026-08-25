# -*- coding: utf-8 -*-
"""OEE Dashboard Config models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_oee_dashboard2(models.Model):
    _name = 'sf.production_oee_dashboard2'
    _description = 'OEE Dashboard Config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    metric = fields.Char(string='Metric', required=True)
    metric_type = fields.Selection([
        ('availability', 'Availability'),
        ('performance', 'Performance'),
        ('quality', 'Quality'),
        ('oee', 'OEE'),
        ], string='Type', required=True)
    target = fields.Float(string='Target %')
    alert_threshold = fields.Float(string='Alert Threshold %')
    workcenter_filter = fields.Char(string='Work Center Filter')
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
                    'sf.production_oee_dashboard2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

