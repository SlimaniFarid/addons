# -*- coding: utf-8 -*-
from odoo import fields, models


class HseResCompany(models.Model):
    _inherit = 'res.company'

    sf_hse_last_major_incident = fields.Datetime(
        string='Last Major/Critical Incident')