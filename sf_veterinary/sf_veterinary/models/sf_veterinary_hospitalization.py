# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVeterinaryHospitalization(models.Model):
    _name = 'sf.veterinary.hospitalization'
    _description = 'Veterinary Hospitalization'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    patient_id = fields.Many2one(
        'sf.veterinary.patient', string='Patient', ondelete='restrict',
        required=True, index=True, tracking=True)
    admission_date = fields.Datetime(
        string='Admission', default=fields.Datetime.now, tracking=True)
    discharge_date = fields.Datetime(string='Discharge', tracking=True)
    cage = fields.Char(string='Cage/Box', tracking=True)
    reason = fields.Text(string='Reason', required=True, tracking=True)
    veterinarian_id = fields.Many2one(
        'res.partner', string='Veterinarian', ondelete='set null',
        domain="[('sf_veterinary_is_veterinarian', '=', True)]",
        tracking=True)
    state = fields.Selection([
        ('admitted', 'Admitted'),
        ('in_progress', 'In Progress'),
        ('discharged', 'Discharged'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='admitted', required=True, tracking=True,
       index=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.veterinary.hospitalization')
        return super().create(vals)

    def action_confirm(self):
        for hospitalization in self:
            if hospitalization.state != 'admitted':
                raise UserError(_('Only admitted hospitalizations can be '
                                  'started.'))
        self.state = 'in_progress'

    def action_discharge(self):
        for hospitalization in self:
            if hospitalization.state != 'in_progress':
                raise UserError(_('Only in-progress hospitalizations can be '
                                  'discharged.'))
            if hospitalization.discharge_date and \
                    hospitalization.admission_date and \
                    hospitalization.discharge_date < hospitalization.admission_date:
                raise UserError(_('The discharge date cannot be earlier than '
                                  'the admission date.'))
            if not hospitalization.discharge_date:
                hospitalization.discharge_date = fields.Datetime.now()
        self.state = 'discharged'

    def action_cancel(self):
        if not self.env.user.has_group(
                'sf_veterinary.group_sf_veterinary_manager'):
            raise UserError(_('Only a veterinary manager can cancel '
                              'hospitalizations.'))
        for hospitalization in self:
            if hospitalization.state == 'cancelled':
                raise UserError(_('This hospitalization is already '
                                  'cancelled.'))
        self.state = 'cancelled'
