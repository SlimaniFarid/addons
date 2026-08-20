# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class TrainingRegistration(models.Model):
    _name = 'sf.training.registration'
    _description = 'Training Registration'
    _order = 'session_id, employee_id'

    session_id = fields.Many2one('sf.training.session',
                                 string='Session', required=True,
                                 ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    state = fields.Selection([
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('completed', 'Completed'),
    ], string='Status', default='registered')
    certificate_id = fields.Many2one('sf.employee.certification',
                                     string='Certificate')

    def action_mark_completed(self):
        for registration in self:
            if registration.state != 'attended':
                raise UserError(
                    _('Only attended registrations can be '
                      'marked as completed.'))
            registration.state = 'completed'