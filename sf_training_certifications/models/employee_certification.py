# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EmployeeCertification(models.Model):
    _name = 'sf.employee.certification'
    _description = 'Employee Certification'
    _inherit = ['mail.thread']
    _order = 'issue_date desc'
    _sql_constraints = [
        ('cert_unique', 'UNIQUE (employee_id, training_id, '
         'certificate_number)',
         'A certificate already exists for this employee, '
         'training and number.'),
    ]

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    training_id = fields.Many2one('sf.training', string='Training',
                                  required=True)
    registration_id = fields.Many2one('sf.training.registration',
                                      string='Registration')
    certificate_number = fields.Char(string='Certificate Number')
    issue_date = fields.Date(string='Issue Date', required=True)
    expiration_date = fields.Date(string='Expiration Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    @api.constrains('issue_date', 'expiration_date')
    def _check_dates(self):
        for cert in self:
            if cert.expiration_date and \
                    cert.expiration_date < cert.issue_date:
                raise UserError(
                    _('The expiration date cannot be before the '
                      'issue date.'))

    @api.constrains('registration_id', 'training_id')
    def _check_registration_training(self):
        for cert in self:
            if cert.registration_id and \
                    cert.registration_id.session_id.training_id.id \
                    != cert.training_id.id:
                raise UserError(
                    _('The registration does not belong to the '
                      'selected training.'))

    def action_issue(self):
        for cert in self:
            if cert.state != 'draft':
                raise UserError(
                    _('Only draft certificates can be issued.'))
            cert.state = 'active'
            if cert.registration_id:
                cert.registration_id.state = 'completed'

    def action_renew(self):
        for cert in self:
            if cert.state not in ('active', 'expiring'):
                raise UserError(
                    _('Only active or expiring certificates can '
                      'be renewed.'))
            cert.state = 'renewed'
            cert.message_post(body=_('Certificate renewed.'))

    def _cron_check_expiration(self):
        today = fields.Date.today()
        soon = today + timedelta(days=30)
        certs = self.search([('state', 'in', ('active', 'expiring'))])
        for cert in certs:
            if not cert.expiration_date:
                continue
            if cert.expiration_date < today:
                cert.state = 'expired'
            elif cert.expiration_date <= soon:
                if cert.state == 'active':
                    cert.state = 'expiring'
                    cert.activity_schedule(
                        'mail.mail_activity_data_todo',
                        _('Certification %s expires soon.') %
                        cert.certificate_number,
                        user_id=cert.env.user.id)