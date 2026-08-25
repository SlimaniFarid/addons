# -*- coding: utf-8 -*-
"""Production Waste Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_waste_tracker(models.Model):
    _name = 'sf.production_waste_tracker'
    _description = 'Production Waste Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order', required=True)
    waste_type = fields.Selection([
        ('material', 'Material'),
        ('energy', 'Energy'),
        ('time', 'Time'),
        ('packaging', 'Packaging'),
        ], string='Type', required=True)
    quantity = fields.Float(string='Quantity Wasted')
    cost = fields.Monetary(string='Cost')
    reduction_target = fields.Float(string='Reduction Target %')
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
                    'sf.production_waste_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

