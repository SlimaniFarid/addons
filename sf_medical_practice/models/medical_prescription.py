# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMedicalPrescription(models.Model):
    _name = 'sf.medical.prescription'
    _description = 'Medical Prescription'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True, copy=False)
    consultation_id = fields.Many2one('sf.medical.consultation',
                                      string='Consultation', required=True,
                                      ondelete='cascade')
    patient_id = fields.Many2one('sf.medical.patient', string='Patient',
                                 related='consultation_id.patient_id',
                                 store=True, index=True)
    medication = fields.Char(string='Medication', required=True)
    dosage = fields.Char(string='Dosage')
    duration_days = fields.Integer(string='Duration (days)')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='consultation_id.company_id',
                                 store=True, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.medical.prescription')
        return super().create(vals_list)

    def action_issue(self):
        for prescription in self:
            if prescription.state != 'draft':
                raise UserError(_('Only draft prescriptions can be '
                                  'issued.'))
            prescription.state = 'issued'

    def action_close(self):
        for prescription in self:
            if prescription.state != 'issued':
                raise UserError(_('Only issued prescriptions can be '
                                  'closed.'))
        self._check_manager()
        self.state = 'closed'

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_medical_practice.group_sf_medical_manager'):
            raise UserError(_('Only a medical practice manager can close a '
                              'prescription.'))