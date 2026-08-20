# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_oh_alert_days = fields.Integer(
        string='Medical validity alert (days)', default=30)
    sf_oh_auto_create_periodic = fields.Boolean(
        string='Auto-create periodic visits', default=False)
    sf_oh_default_interval_months = fields.Integer(
        string='Default visit periodicity (months)', default=12)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_oh_alert_days = fields.Integer(
        related='company_id.sf_oh_alert_days', readonly=False)
    sf_oh_auto_create_periodic = fields.Boolean(
        related='company_id.sf_oh_auto_create_periodic', readonly=False)
    sf_oh_default_interval_months = fields.Integer(
        related='company_id.sf_oh_default_interval_months', readonly=False)