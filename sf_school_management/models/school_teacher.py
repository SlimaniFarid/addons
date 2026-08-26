# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolTeacher(models.Model):
    _name = 'sf.school.teacher'
    _description = 'School Teacher'
    _order = 'name'

    name = fields.Char(string='Teacher', required=True, index=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  ondelete='restrict')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.teacher')
        return super().create(vals)