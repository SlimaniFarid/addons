# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SfSeniorResident(models.Model):
    _name = 'sf.senior.resident'
    _description = 'Senior Resident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Full Name', required=True)
    residence_id = fields.Many2one('sf.senior.residence',
                                   string='Residence', required=True,
                                   ondelete='restrict')
    partner_id = fields.Many2one('res.partner', string='Related Contact')
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    room_number = fields.Char(string='Room Number')
    gir_level = fields.Integer(string='GIR Level (1-6)',
                               help='Autonomy level: 1=dependent, '
                                    '6=autonomous')
    admission_date = fields.Date(string='Admission Date',
                                 default=fields.Date.today)
    discharge_date = fields.Date(string='Discharge Date')
    emergency_contact = fields.Char(string='Emergency Contact')
    medical_notes = fields.Html(string='Medical Notes')
    state = fields.Selection([
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('deceased', 'Deceased'),
    ], string='Status', default='admitted', tracking=True)
    company_id = fields.Many2one(related='residence_id.company_id',
                                 store=True)

    @api.constrains('gir_level')
    def _check_gir_level(self):
        for rec in self:
            if rec.gir_level and not (1 <= rec.gir_level <= 6):
                raise _('%s: GIR level must be between 1 and 6.') % rec.name
