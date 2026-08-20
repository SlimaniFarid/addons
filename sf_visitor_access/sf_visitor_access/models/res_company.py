# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_visitor_alert_hours = fields.Integer(
        string='Visitor overtime alert (hours)', default=1)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_visitor_alert_hours = fields.Integer(
        related='company_id.sf_visitor_alert_hours', readonly=False)