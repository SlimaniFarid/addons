# -*- coding: utf-8 -*-
from odoo import fields, models


class RoutesResCompany(models.Model):
    _inherit = 'res.company'

    sf_route_auto_missed = fields.Boolean(
        string='Auto-mark Missed Visits', default=True)


class RoutesResPartner(models.Model):
    _inherit = 'res.partner'

    sf_territory_id = fields.Many2one('sf.route.territory',
                                      string='Territory')