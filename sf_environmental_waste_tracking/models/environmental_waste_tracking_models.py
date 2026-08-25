# -*- coding: utf-8 -*-
"""Environmental Waste Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEnvironmental_waste_tracking(models.Model):
    _name = 'sf.environmental_waste_tracking'
    _description = 'Environmental Waste Tracking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    site = fields.Char(string='Site', required=True)
    waste_type = fields.Selection([
        ('paper', 'Paper'),
        ('plastic', 'Plastic'),
        ('metal', 'Metal'),
        ('electronic', 'Electronic'),
        ('chemical', 'Chemical'),
        ('organic', 'Organic'),
        ], string='Waste Type', required=True)
    quantity_kg = fields.Float(string='Quantity (kg)')
    disposal_method = fields.Char(string='Disposal Method')
    cost = fields.Monetary(string='Cost')
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
                    'sf.environmental_waste_tracking') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

