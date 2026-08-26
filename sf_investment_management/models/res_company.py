# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_invest_alert_days = fields.Integer(
        string='Maturity alert margin (days)', default=15)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_invest_alert_days = fields.Integer(
        related='company_id.sf_invest_alert_days', readonly=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.invest.portfolio'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
