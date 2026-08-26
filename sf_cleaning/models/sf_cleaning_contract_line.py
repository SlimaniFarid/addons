# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfCleaningContractLine(models.Model):
    _name = 'sf.cleaning.contract.line'
    _description = 'Cleaning Contract Line'
    _order = 'id'

    contract_id = fields.Many2one(
        'sf.cleaning.contract', string='Contract', ondelete='cascade',
        required=True, index=True)
    company_id = fields.Many2one(
        'res.company', string='Company', related='contract_id.company_id',
        store=True, readonly=True)
    site_id = fields.Many2one(
        'sf.cleaning.site', string='Site', ondelete='restrict',
        required=True, index=True)
    cleaning_type = fields.Selection([
        ('standard', 'Standard'),
        ('deep', 'Deep'),
        ('window', 'Window'),
        ('floor', 'Floor'),
    ], string='Cleaning type', default='standard', required=True)
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('monthly', 'Monthly'),
    ], string='Frequency', default='weekly', required=True)
    interval_days = fields.Integer(
        string='Interval days', compute='_compute_interval_days', store=True)
    planned_qty = fields.Float(string='Planned quantity', default=1.0)
    unit_price = fields.Monetary(
        string='Unit price', currency_field='currency_id', default=0.0)
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id, required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.depends('frequency')
    def _compute_interval_days(self):
        mapping = {'daily': 1, 'weekly': 7, 'biweekly': 14, 'monthly': 30}
        for line in self:
            line.interval_days = mapping.get(line.frequency, 7)