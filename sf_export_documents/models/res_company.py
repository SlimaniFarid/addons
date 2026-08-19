# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_export_origin_country_id = fields.Many2one(
        'res.country', string='Default country of origin')
    sf_export_alert_days = fields.Integer(
        string='Export preparation alert (days)', default=3)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_export_origin_country_id = fields.Many2one(
        'res.country', related='company_id.sf_export_origin_country_id',
        readonly=False)
    sf_export_alert_days = fields.Integer(
        related='company_id.sf_export_alert_days', readonly=False)