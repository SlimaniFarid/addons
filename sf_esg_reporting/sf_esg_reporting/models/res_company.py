# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_esg_default_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Default period frequency', default='monthly')
    sf_esg_default_company = fields.Boolean(
        string='ESG reporting company', default=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_esg_default_frequency = fields.Selection(
        related='company_id.sf_esg_default_frequency', readonly=False)
    sf_esg_default_company = fields.Boolean(
        related='company_id.sf_esg_default_company', readonly=False)