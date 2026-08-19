# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SchoolGrade(models.Model):
    _name = 'sf.school.grade'
    _description = 'Student Grade'
    _order = 'student_id, course_id, id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Grade', required=True, index=True)
    student_id = fields.Many2one('sf.school.student', string='Student',
                                 required=True, ondelete='restrict',
                                 index=True)
    course_id = fields.Many2one('sf.school.course', string='Course',
                                required=True, ondelete='restrict',
                                index=True)
    period = fields.Char(string='Period')
    grade = fields.Float(string='Grade')
    coefficient = fields.Float(string='Coefficient', default=1.0)
    comment = fields.Text(string='Comment')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('student_course_period_uniq',
         'UNIQUE(student_id, course_id, period)',
         _('This grade period already exists for this student and '
           'course.')),
    ]

    @api.constrains('grade', 'coefficient')
    def _check_values(self):
        for rec in self:
            if rec.grade < 0 or rec.grade > 20:
                raise ValidationError(
                    _('Grade must be between 0 and 20.'))
            if rec.coefficient <= 0:
                raise ValidationError(_('Coefficient must be positive.'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.grade')
        return super().create(vals)

    def action_confirm(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_school_management.group_school_manager'):
            raise UserError(_('Only a School Manager can confirm grades.'))
        if self.state != 'draft':
            raise UserError(_('Only draft grades can be confirmed.'))
        self.state = 'confirmed'