# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SchoolAbsence(models.Model):
    _name = 'sf.school.absence'
    _description = 'Student Absence'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Absence', required=True, index=True)
    student_id = fields.Many2one('sf.school.student', string='Student',
                                 required=True, ondelete='restrict',
                                 index=True)
    course_id = fields.Many2one('sf.school.course', string='Course',
                                required=True, ondelete='restrict')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    reason = fields.Selection([
        ('illness', 'Illness'),
        ('family', 'Family reason'),
        ('appointment', 'Appointment'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ], string='Reason')
    justified = fields.Boolean(string='Justified', default=False)
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('justified', 'Justified'),
        ('unjustified', 'Unjustified'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.absence')
        return super().create(vals)

    def action_set_justified(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft absences can be justified.'))
        self.write({'state': 'justified', 'justified': True})

    def action_set_unjustified(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft absences can be marked as '
                              'unjustified.'))
        self.write({'state': 'unjustified', 'justified': False})