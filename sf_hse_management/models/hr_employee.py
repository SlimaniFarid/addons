# -*- coding: utf-8 -*-
from odoo import fields, models


class HseHrEmployee(models.Model):
    _inherit = 'hr.employee'

    sf_hse_incident_ids = fields.One2many('sf.hse.incident',
                                          'employee_id',
                                          string='Incidents')
    sf_hse_ppe_ids = fields.One2many('sf.hse.ppe', 'employee_id',
                                     string='PPE Equipment')