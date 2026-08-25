# -*- coding: utf-8 -*-
"""Energy Meter Readings & Alerts models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEnergyReading(models.Model):
    _name = 'sf.energy.meter.reading'
    _description = 'Meter Reading'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    site = fields.Char(string='Site', required=True)
    meter_ref = fields.Char(string='Meter Ref', required=True)
    period_month = fields.Date(string='Period', required=True)
    reading = fields.Float(string='Reading')
    consumption = fields.Float(string='Consumption')
    anomaly = fields.Boolean(string='Anomaly Detected')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('recorded', 'Recorded'),
        ('validated', 'Validated'),
        ], string='Status', default='recorded', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.energy.meter.reading') or 'NEW'
        return super().create(vals_list)

    def action_validated(self):
        self.write({'state': 'validated'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.energy.meter.reading'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
