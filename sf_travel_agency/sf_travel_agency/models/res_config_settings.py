# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_travel_agency_commission_rate = fields.Float(
        string='Default Commission Rate (%)',
        default=10.0,
        config_parameter='sf_travel_agency.commission_rate',
    )
    sf_travel_agency_reminder_days = fields.Integer(
        string='Departure Reminder (Days)',
        default=7,
        config_parameter='sf_travel_agency.reminder_days',
    )

    @api.model
    def set_values(self):
        previous = self.sf_travel_agency_commission_rate
        super().set_values()
        new_rate = float(self.env['ir.config_parameter'].sudo().get_param(
            'sf_travel_agency.commission_rate', '10.0'
        ) or 10.0)
        if previous != new_rate:
            reservations = self.env['sf.travel.reservation'].search([('state', 'not in', ('cancelled',))])
            reservations._compute_commission()