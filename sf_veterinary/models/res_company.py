# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_veterinary_vaccination_due_days = fields.Integer(
        string='Vaccination due days', default=365)
    sf_veterinary_reminder_days = fields.Integer(
        string='Vaccination reminder days', default=30)
    sf_veterinary_default_duration_minutes = fields.Integer(
        string='Default appointment duration (minutes)', default=30)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_veterinary_vaccination_due_days = fields.Integer(
        related='company_id.sf_veterinary_vaccination_due_days',
        readonly=False)
    sf_veterinary_reminder_days = fields.Integer(
        related='company_id.sf_veterinary_reminder_days', readonly=False)
    sf_veterinary_default_duration_minutes = fields.Integer(
        related='company_id.sf_veterinary_default_duration_minutes',
        readonly=False)
