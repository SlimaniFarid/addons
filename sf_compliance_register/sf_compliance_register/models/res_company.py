# -*- coding: utf-8 -*-
from odoo import fields, models


class ComplianceResCompany(models.Model):
    _inherit = 'res.company'

    sf_compliance_default_alert_days = fields.Integer(
        string='Default Alert Days', default=30)
    sf_compliance_require_attachment = fields.Boolean(
        string='Require Attachment at Publication', default=False)