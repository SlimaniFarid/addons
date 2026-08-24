# -*- coding: utf-8 -*-
"""Energy Saving Initiative Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEnergy_saving_tracker(models.Model):
    _name = 'sf.energy_saving_tracker'
    _description = 'Energy Saving Initiative Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    initiative = fields.Char(string='Initiative', required=True)
    investment = fields.Monetary(string='Investment')
    annual_saving = fields.Monetary(string='Annual Saving')
    payback_years = fields.Float(string='Payback (years)')
    co2_reduction_tons = fields.Float(string='CO2 Reduction (t/yr)')
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
                    'sf.energy_saving_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

