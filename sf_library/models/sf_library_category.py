# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfLibraryCategory(models.Model):
    _name = 'sf.library.category'
    _description = 'Library Category'
    _order = 'name'

    name = fields.Char(string='Name', required=True, index=True)
    item_ids = fields.One2many('sf.library.item', 'category_id',
                               string='Items')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.library.category')
        return super().create(vals)
