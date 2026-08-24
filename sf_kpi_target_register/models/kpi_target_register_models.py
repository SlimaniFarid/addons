# -*- coding: utf-8 -*-
"""KPI Definition & Target Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfKpiDefinition(models.Model):
    _name = 'sf.kpi.definition'
    _description = 'KPI Definition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    kpi_name = fields.Char(string='KPI Name', required=True)
    formula = fields.Text(string='Formula / Source', required=True)
    owner_id = fields.Many2one('res.users', string='KPI Owner')
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ], string='Frequency', default=monthly)
    target_value = fields.Float(string='Target')
    actual_value = fields.Float(string='Actual')
    unit = fields.Char(string='Unit')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('under_review', 'Under Review'),
        ('retired', 'Retired'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.kpi.definition') or 'NEW'
        return super().create(vals_list)

    def action_under_review(self):
        self.write({'state': 'under_review'})

    def action_retired(self):
        self.write({'state': 'retired'})

