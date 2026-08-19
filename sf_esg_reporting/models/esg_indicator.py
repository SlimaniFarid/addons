# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EsgIndicator(models.Model):
    _name = 'sf.esg.indicator'
    _description = 'ESG Indicator'
    _order = 'category, code'

    name = fields.Char(string='Name', required=True, index=True)
    code = fields.Char(string='Code', required=True, index=True)
    category = fields.Selection([
        ('environment', 'Environment'),
        ('social', 'Social'),
        ('governance', 'Governance'),
    ], string='Category', required=True)
    unit = fields.Selection([
        ('kwh', 'kWh'),
        ('tco2', 'tCO2e'),
        ('m3', 'm3'),
        ('kg', 'kg'),
        ('eur', 'EUR'),
        ('people', 'People'),
        ('hours', 'Hours'),
        ('pct', '%'),
    ], string='Unit', required=True)
    direction = fields.Selection([
        ('less_is_better', 'Less is better'),
        ('more_is_better', 'More is better'),
    ], string='Direction', required=True)
    frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Frequency', required=True)
    target_source = fields.Char(string='Target source')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('code_uniq', 'UNIQUE(code)',
         _('This indicator code already exists.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.esg.indicator')
            vals['name'] = 'KPI-%s' % seq
        return super().create(vals)