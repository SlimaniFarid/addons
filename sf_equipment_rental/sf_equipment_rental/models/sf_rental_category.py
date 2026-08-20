# -*- coding: utf-8 -*-
from odoo import fields, models


class SfRentalCategory(models.Model):
    _name = 'sf.rental.category'
    _description = 'Rental Equipment Category'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.rental.category')
        return super().create(vals_list)