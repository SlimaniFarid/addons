# -*- coding: utf-8 -*-
"""Waste Stream Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfWaste_stream_tracker(models.Model):
    _name = 'sf.waste_stream_tracker'
    _description = 'Waste Stream Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    site = fields.Char(string='Site', required=True)
    waste_type = fields.Selection([
        ('paper', 'Paper'),
        ('plastic', 'Plastic'),
        ('metal', 'Metal'),
        ('organic', 'Organic'),
        ('hazardous', 'Hazardous'),
        ], string='Type', required=True)
    quantity_kg = fields.Float(string='Quantity (kg)')
    disposal_cost = fields.Monetary(string='Disposal Cost')
    recycled = fields.Boolean(string='Recycled')
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
                    'sf.waste_stream_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

