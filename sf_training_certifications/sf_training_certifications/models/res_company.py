# -*- coding: utf-8 -*-
from odoo import fields, models


class TrainingResCompany(models.Model):
    _inherit = 'res.company'

    sf_cert_alert_days = fields.Integer(
        string='Certification Expiry Alert (days)', default=30,
        help='Days before expiration when a certification is '
             'flagged as expiring.')