# -*- coding: utf-8 -*-
from odoo import fields, models


class TrainingHrEmployee(models.Model):
    _inherit = 'hr.employee'

    sf_training_registration_ids = fields.One2many(
        'sf.training.registration', 'employee_id',
        string='Trainings')
    sf_certification_ids = fields.One2many(
        'sf.employee.certification', 'employee_id',
        string='Certifications')