# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sf_trade_instrument_ids = fields.Many2many(
        'sf.trade.instrument', string='Trade Finance Instruments')


class AccountMove(models.Model):
    _inherit = 'account.move'

    sf_trade_instrument_ids = fields.Many2many(
        'sf.trade.instrument', string='Trade Finance Instruments')


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_trade_alert_days = fields.Integer(
        string='Instrument expiry alert (days)', default=30)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_trade_alert_days = fields.Integer(
        related='company_id.sf_trade_alert_days', readonly=False)