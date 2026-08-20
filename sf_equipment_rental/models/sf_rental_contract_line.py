# -*- coding: utf-8 -*-
import math

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfRentalContractLine(models.Model):
    _name = 'sf.rental.contract.line'
    _description = 'Rental Contract Line'
    _order = 'id asc'

    contract_id = fields.Many2one('sf.rental.contract', string='Contract', required=True, ondelete='cascade')
    equipment_id = fields.Many2one('sf.rental.equipment', string='Equipment', required=True, ondelete='restrict')
    price_unit = fields.Monetary(string='Unit Price', compute='_compute_price_unit', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    qty = fields.Integer(string='Quantity', default=1)
    subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, currency_field='currency_id')
    tier = fields.Selection([
        ('auto', 'Automatic'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], string='Pricing Tier', default='auto')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('contract_id.start_datetime', 'contract_id.end_datetime', 'equipment_id',
                 'equipment_id.hourly_price', 'equipment_id.daily_price',
                 'equipment_id.weekly_price', 'equipment_id.monthly_price', 'tier')
    def _compute_price_unit(self):
        for line in self:
            equipment = line.equipment_id
            start = line.contract_id.start_datetime
            end = line.contract_id.end_datetime
            if not start or not end:
                line.price_unit = 0.0
                continue
            duration_hours = (end - start).total_seconds() / 3600.0
            hourly = equipment.hourly_price or 0.0
            daily = equipment.daily_price or 0.0
            weekly = equipment.weekly_price or 0.0
            monthly = equipment.monthly_price or 0.0
            days = max(1, math.ceil(duration_hours / 24.0))
            weeks = max(1, math.ceil(duration_hours / (24 * 7)))
            force = line.tier
            if force == 'hourly':
                price = hourly * duration_hours
            elif force == 'daily':
                price = daily * days
            elif force == 'weekly':
                price = weekly * weeks
            elif force == 'monthly':
                price = monthly
            elif duration_hours < 24:
                price = hourly * duration_hours
            elif duration_hours <= 7 * 24:
                price = daily * days
                if weekly:
                    price = min(price, weekly)
            elif duration_hours <= 30 * 24:
                price = weekly * weeks
            else:
                price = monthly
            line.price_unit = price

    @api.depends('price_unit', 'qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.price_unit * line.qty

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('qty', 1) <= 0:
                raise UserError(_('Quantities must be strictly positive.'))
            if vals.get('contract_id') and not vals.get('company_id'):
                contract = self.env['sf.rental.contract'].browse(vals['contract_id'])
                vals['company_id'] = contract.company_id.id
        return super().create(vals_list)

    def write(self, vals):
        if 'qty' in vals and vals.get('qty', 0) <= 0:
            raise UserError(_('Quantities must be strictly positive.'))
        return super().write(vals)