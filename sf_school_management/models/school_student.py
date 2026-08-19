# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SchoolStudent(models.Model):
    _name = 'sf.school.student'
    _description = 'School Student'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Student', required=True, index=True)
    birth_date = fields.Date(string='Birth date')
    tutor_ids = fields.Many2many('res.partner', string='Tutors')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    group_id = fields.Many2one('sf.school.group', string='Group',
                               ondelete='restrict', index=True)
    enrollment_date = fields.Date(string='Enrollment date')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.student')
        return super().create(vals)

    @api.constrains('state', 'group_id')
    def _check_active_group(self):
        for rec in self:
            if rec.state == 'active' and not rec.group_id:
                raise ValidationError(
                    _('An active student must be assigned to a group.'))

    def action_activate(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft students can be activated.'))
        if not self.group_id:
            raise UserError(
                _('An active student must be assigned to a group.'))
        self.state = 'active'

    def action_deactivate(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active students can be deactivated.'))
        self.state = 'inactive'

    def get_weighted_average(self):
        self.ensure_one()
        grades = self.env['sf.school.grade'].search([
            ('student_id', '=', self.id),
            ('state', '=', 'confirmed'),
        ])
        total = sum(grade.grade * grade.coefficient for grade in grades)
        coef = sum(grade.coefficient for grade in grades)
        return round(total / coef, 2) if coef else 0.0

    def get_subject_averages(self):
        self.ensure_one()
        grades = self.env['sf.school.grade'].search([
            ('student_id', '=', self.id),
            ('state', '=', 'confirmed'),
        ])
        averages = {}
        for grade in grades:
            course = grade.course_id
            entry = averages.setdefault(course.id, {
                'course': course.name,
                'subject': course.subject or '',
                'grade_list': [],
                'weighted': 0.0,
                'coef': 0.0,
            })
            entry['grade_list'].append(grade.grade)
            entry['weighted'] += grade.grade * grade.coefficient
            entry['coef'] += grade.coefficient
        result = []
        for entry in averages.values():
            entry['average'] = round(
                entry['weighted'] / entry['coef'], 2) if entry['coef'] else 0.0
            entry['grade_list'] = ', '.join(
                str(value) for value in entry['grade_list'])
            result.append(entry)
        return result