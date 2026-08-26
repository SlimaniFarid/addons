# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    salon_package_ids = fields.One2many('sf.salon.package', 'partner_id', string='Salon Packages')