# -*- coding: utf-8 -*-
from odoo import fields, models


class SfBusinessTravelLine(models.Model):
    _name = 'sf.business.travel.line'
    _description = 'Business Travel Line'
    _order = 'line_date asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    travel_id = fields.Many2one(
        'sf.business.travel', string='Travel', required=True,
        ondelete='cascade')
    line_date = fields.Date(string='Date')
    line_type = fields.Selection([
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('hotel', 'Hotel'),
        ('car', 'Car'),
        ('other', 'Other'),
    ], string='Type', default='other')
    description = fields.Char(string='Description')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.business.travel.line')
            if vals.get('travel_id') and not vals.get('company_id'):
                travel = self.env['sf.business.travel'].browse(
                    vals['travel_id'])
                vals['company_id'] = travel.company_id.id
        return super().create(vals_list)