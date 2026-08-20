# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_donation_reminder_days = fields.Integer(
        string='Pledge reminder days', default=7)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_donation_reminder_days = fields.Integer(
        related='company_id.sf_donation_reminder_days', readonly=False)