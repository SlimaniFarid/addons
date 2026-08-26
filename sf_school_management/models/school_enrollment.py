# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SchoolEnrollment(models.Model):
    _name = 'sf.school.enrollment'
    _description = 'Course Enrollment'
    _order = 'id desc'

    name = fields.Char(string='Enrollment', required=True, index=True)
    student_id = fields.Many2one('sf.school.student', string='Student',
                                 required=True, ondelete='restrict',
                                 index=True)
    course_id = fields.Many2one('sf.school.course', string='Course',
                                required=True, ondelete='restrict',
                                index=True)
    year_id = fields.Many2one('sf.school.year', string='School year',
                              required=True, ondelete='restrict')
    date = fields.Date(string='Enrollment date',
                       default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('student_course_year_uniq',
         'UNIQUE(student_id, course_id, year_id)',
         _('This student is already enrolled in this course for this '
           'year.')),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.enrollment')
        return super().create(vals)