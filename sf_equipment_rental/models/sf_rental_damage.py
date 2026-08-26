# -*- coding: utf-8 -*-
from odoo import fields, models


class SfRentalDamage(models.Model):
    _name = 'sf.rental.damage'
    _description = 'Rental Damage'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    inspection_id = fields.Many2one('sf.rental.inspection', string='Inspection', required=True, ondelete='cascade')
    description = fields.Char(string='Description', required=True)
    penalty_amount = fields.Monetary(string='Penalty', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.rental.damage')
            if vals.get('inspection_id') and not vals.get('company_id'):
                inspection = self.env['sf.rental.inspection'].browse(vals['inspection_id'])
                vals['company_id'] = inspection.company_id.id
        return super().create(vals_list)