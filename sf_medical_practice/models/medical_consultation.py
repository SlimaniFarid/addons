# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMedicalConsultation(models.Model):
    _name = 'sf.medical.consultation'
    _description = 'Medical Consultation'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True, copy=False)
    patient_id = fields.Many2one('sf.medical.patient', string='Patient',
                                 required=True, ondelete='restrict',
                                 index=True)
    practitioner_id = fields.Many2one('res.users', string='Practitioner',
                                      required=True, ondelete='restrict')
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today, index=True)
    diagnosis = fields.Text(string='Diagnosis')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    prescription_ids = fields.One2many('sf.medical.prescription',
                                       'consultation_id',
                                       string='Prescriptions')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.medical.consultation')
        return super().create(vals_list)

    def action_done(self):
        for consultation in self:
            if consultation.state != 'draft':
                raise UserError(_('Only draft consultations can be '
                                  'validated.'))
        self._check_manager()
        self.state = 'done'

    def action_close(self):
        for consultation in self:
            if consultation.state != 'done':
                raise UserError(_('Only done consultations can be closed.'))
        self._check_manager()
        self.state = 'closed'

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_medical_practice.group_sf_medical_manager'):
            raise UserError(_('Only a medical practice manager can perform '
                              'this action.'))