# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_agri_default_unit = fields.Selection([
        ('kg', 'kg'),
        ('t', 'tonnes'),
    ], string='Default harvest unit', default='kg')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_agri_default_unit = fields.Selection(
        related='company_id.sf_agri_default_unit', readonly=False)