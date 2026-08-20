# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfMedicalPatient(models.Model):
    _name = 'sf.medical.patient'
    _description = 'Medical Patient'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Patient number', required=True, index=True,
                       copy=False)
    firstname = fields.Char(string='First name', required=True, tracking=True)
    lastname = fields.Char(string='Last name', required=True, tracking=True)
    full_name = fields.Char(string='Full name', compute='_compute_full_name',
                            store=True)
    dob = fields.Date(string='Date of birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string='Blood type')
    allergies = fields.Text(string='Allergies')
    insurance = fields.Char(string='Insurance')
    consultation_ids = fields.One2many('sf.medical.consultation',
                                       'patient_id',
                                       string='Consultations')
    appointment_ids = fields.One2many('sf.medical.appointment', 'patient_id',
                                      string='Appointments')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('firstname', 'lastname')
    def _compute_full_name(self):
        for patient in self:
            patient.full_name = ' '.join(
                part for part in (patient.firstname, patient.lastname)
                if part)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.medical.patient')
        return super().create(vals_list)