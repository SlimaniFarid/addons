# -*- coding: utf-8 -*-
from odoo import fields, models


class OnboardingResCompany(models.Model):
    _inherit = 'res.company'

    sf_onboarding_default_template = fields.Many2one(
        'sf.onboarding.template', string='Default Onboarding Template')
    sf_offboarding_default_template = fields.Many2one(
        'sf.onboarding.template', string='Default Offboarding Template')