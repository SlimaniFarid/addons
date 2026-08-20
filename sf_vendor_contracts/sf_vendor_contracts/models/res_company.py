# -*- coding: utf-8 -*-
from odoo import fields, models


class VendorContractResCompany(models.Model):
    _inherit = 'res.company'

    sf_contract_alert_days = fields.Integer(
        string='Contract Expiry Alert (days)', default=60,
        help='Days before the end date when a contract is '
             'flagged as expiring.')