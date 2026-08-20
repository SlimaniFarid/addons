# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sf_veterinary_is_veterinarian = fields.Boolean(
        string='Veterinarian', default=False)
