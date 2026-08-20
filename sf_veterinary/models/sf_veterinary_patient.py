# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVeterinaryPatient(models.Model):
    _name = 'sf.veterinary.patient'
    _description = 'Veterinary Patient'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    species = fields.Selection([
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ], string='Species', required=True, tracking=True)
    breed = fields.Char(string='Breed', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    birth_date = fields.Date(string='Birth date', tracking=True)
    age_months = fields.Integer(
        string='Age (months)', compute='_compute_age_months', store=True)
    weight_kg = fields.Float(string='Weight (kg)', tracking=True)
    sterilized = fields.Boolean(string='Sterilized', tracking=True)
    allergies = fields.Text(string='Allergies')
    owner_id = fields.Many2one(
        'res.partner', string='Owner', ondelete='set null', tracking=True)
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')
    vaccination_ids = fields.One2many(
        'sf.veterinary.vaccination', 'patient_id', string='Vaccinations',
        inverse_depends=['state', 'next_due_date'])
    vaccinations_ok = fields.Boolean(
        string='Vaccinations up to date', compute='_compute_vaccinations_ok',
        store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deceased', 'Deceased'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('birth_date')
    def _compute_age_months(self):
        today = fields.Date.context_today(self)
        for patient in self:
            if not patient.birth_date:
                patient.age_months = 0
                continue
            months = (today.year - patient.birth_date.year) * 12 + \
                today.month - patient.birth_date.month
            if today.day < patient.birth_date.day:
                months -= 1
            patient.age_months = max(0, months)

    @api.depends('vaccination_ids.state', 'vaccination_ids.next_due_date')
    def _compute_vaccinations_ok(self):
        today = fields.Date.context_today(self)
        for patient in self:
            patient.vaccinations_ok = any(
                v.state == 'administered' and v.next_due_date
                and v.next_due_date >= today
                for v in patient.vaccination_ids)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.veterinary.patient')
        return super().create(vals)

    def action_activate(self):
        for patient in self:
            if patient.state != 'draft':
                raise UserError(_('Only draft patients can be activated.'))
        self.write({'state': 'active', 'active': True})

    def action_archive_patient(self):
        if not self.env.user.has_group(
                'sf_veterinary.group_sf_veterinary_manager'):
            raise UserError(_('Only a veterinary manager can archive '
                              'patients.'))
        for patient in self:
            if patient.state != 'active':
                raise UserError(_('Only active patients can be archived.'))
        self.write({'state': 'archived', 'active': False})

    def action_deceased(self):
        for patient in self:
            if patient.state != 'active':
                raise UserError(_('Only active patients can be marked as '
                                  'deceased.'))
        self.write({'state': 'deceased', 'active': False})
