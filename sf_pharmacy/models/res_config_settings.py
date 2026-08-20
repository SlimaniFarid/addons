# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_pharmacy_expiry_days = fields.Integer(string='Expiry alert delay (days)', default=90)
    sf_pharmacy_low_stock_threshold = fields.Float(string='Low stock threshold', default=5.0)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        icp = self.env['ir.config_parameter'].sudo()
        res.update(
            sf_pharmacy_expiry_days=int(icp.get_param('sf_pharmacy.expiry_days', default='90')),
            sf_pharmacy_low_stock_threshold=float(icp.get_param('sf_pharmacy.low_stock_threshold', default='5.0')),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('sf_pharmacy.expiry_days', str(self.sf_pharmacy_expiry_days))
        icp.set_param('sf_pharmacy.low_stock_threshold', str(self.sf_pharmacy_low_stock_threshold))
