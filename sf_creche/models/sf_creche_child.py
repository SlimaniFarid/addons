# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CrecheChild(models.Model):
    _name = 'sf.creche.child'
    _description = 'Creche Child'
    _order = 'name'

    name = fields.Char(string='Child', required=True, index=True)
    firstname = fields.Char(string='First name')
    lastname = fields.Char(string='Last name')
    dob = fields.Date(string='Date of birth')
    parents = fields.Char(string='Parents')
    parent_ids = fields.Many2many('res.partner', string='Family contacts')
    emergency_phone = fields.Char(string='Emergency phone')
    allergies = fields.Text(string='Allergies')
    active = fields.Boolean(string='Active', default=True)
    enrollment_ids = fields.One2many('sf.creche.enrollment', 'child_id',
                                     string='Enrollments')
    attendance_ids = fields.One2many('sf.creche.attendance', 'child_id',
                                     string='Attendances')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.creche.child')
        return super().create(vals)
