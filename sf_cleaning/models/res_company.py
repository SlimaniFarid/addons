# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_cleaning_alert_enabled = fields.Boolean(
        string='Enable cleaning alerts', default=True)
    sf_cleaning_overdue_days = fields.Integer(
        string='Overdue threshold (days)', default=1)
    sf_cleaning_default_duration = fields.Integer(
        string='Default intervention duration (hours)', default=2)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_cleaning_alert_enabled = fields.Boolean(
        related='company_id.sf_cleaning_alert_enabled', readonly=False)
    sf_cleaning_overdue_days = fields.Integer(
        related='company_id.sf_cleaning_overdue_days', readonly=False)
    sf_cleaning_default_duration = fields.Integer(
        related='company_id.sf_cleaning_default_duration', readonly=False)