# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sf_oh_medical_file_ids = fields.One2many('sf.oh.medical.file',
                                             'employee_id',
                                             string='Medical Files')
    sf_oh_medical_file_id = fields.Many2one(
        'sf.oh.medical.file', string='Occupational Health File',
        compute='_compute_sf_oh_medical_file')
    sf_oh_last_aptitude = fields.Selection(
        [('apt', 'Fit'),
         ('apt_restricted', 'Fit with restrictions'),
         ('inapt', 'Unfit')],
        string='Last aptitude',
        related='sf_oh_medical_file_id.last_aptitude', readonly=True)

    def _compute_sf_oh_medical_file(self):
        for employee in self:
            employee.sf_oh_medical_file_id = employee.sf_oh_medical_file_ids[
                :1]