# -*- coding: utf-8 -*-
"""Warehouse Zone Capacity Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfZoneCapacity(models.Model):
    _name = 'sf.zone.capacity'
    _description = 'Zone Capacity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    zone_name = fields.Char(string='Zone', required=True)
    max_pallets = fields.Integer(string='Max Pallets', required=True)
    current_pallets = fields.Integer(string='Current Pallets')
    occupancy_percent = fields.Float(string='Occupancy %')
    relocation_note = fields.Text(string='Relocation Suggestions')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('critical', 'Critical'),
        ('resolved', 'Resolved'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.zone.capacity') or 'NEW'
        return super().create(vals_list)

    def action_critical(self):
        self.write({'state': 'critical'})

    def action_resolved(self):
        self.write({'state': 'resolved'})

