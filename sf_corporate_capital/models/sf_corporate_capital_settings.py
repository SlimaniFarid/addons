# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_capital_default_nominal_value = fields.Monetary(
        string='Default Nominal Value',
        config_parameter='sf_corporate_capital.default_nominal_value',
        company_dependent=True,
        help='Default nominal value for new share classes')
    sf_capital_default_authorized_shares = fields.Integer(
        string='Default Authorized Shares',
        config_parameter='sf_corporate_capital.default_authorized_shares',
        company_dependent=True,
        help='Default authorized shares for new share classes')