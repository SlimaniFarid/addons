# -*- coding: utf-8 -*-
from odoo import fields, models, _


class PartnerExt(models.Model):
    _inherit = 'res.partner'

    price_matrix_category_id = fields.Many2one(
        'sf.price.matrix.category', string='Price Matrix Category')