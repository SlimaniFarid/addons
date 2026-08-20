# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class CertificationIssueWizard(models.TransientModel):
    _name = 'sf.certification.issue.wizard'
    _description = 'Issue Certificates Wizard'

    session_id = fields.Many2one('sf.training.session',
                                 string='Session', required=True,
                                 readonly=True)
    issue_date = fields.Date(string='Issue Date',
                             required=True,
                             default=fields.Date.today)
    expiration_date = fields.Date(string='Expiration Date')

    def action_issue(self):
        self.ensure_one()
        session = self.session_id
        if session.state != 'done':
            raise UserError(
                _('Certificates can only be issued for a done '
                  'session.'))
        certs = self.env['sf.employee.certification']
        for registration in session.registration_ids:
            existing = self.env['sf.employee.certification'].search([
                ('employee_id', '=', registration.employee_id.id),
                ('training_id', '=', session.training_id.id),
                ('state', '!=', 'renewed'),
            ], limit=1)
            if existing:
                continue
            certs.create({
                'employee_id': registration.employee_id.id,
                'training_id': session.training_id.id,
                'registration_id': registration.id,
                'issue_date': self.issue_date,
                'expiration_date': self.expiration_date,
                'certificate_number': '%s-%s-%s' % (
                    session.training_id.name[:3].upper(),
                    registration.employee_id.id,
                    registration.id),
                'state': 'active',
            })
            registration.state = 'completed'
        return {'type': 'ir.actions.act_window_close'}


class CertificationRenewWizard(models.TransientModel):
    _name = 'sf.certification.renew.wizard'
    _description = 'Renew Certification Wizard'

    certification_id = fields.Many2one('sf.employee.certification',
                                       string='Certification',
                                       required=True, readonly=True)
    new_issue_date = fields.Date(string='New Issue Date',
                                 required=True,
                                 default=fields.Date.today)
    new_expiration_date = fields.Date(string='New Expiration Date')

    def action_renew(self):
        self.ensure_one()
        old = self.certification_id
        if old.state not in ('active', 'expiring'):
            raise UserError(
                _('Only active or expiring certificates can be '
                  'renewed.'))
        old.state = 'renewed'
        old.message_post(body=_('Certificate renewed.'))
        new_cert = self.env['sf.employee.certification'].create({
            'employee_id': old.employee_id.id,
            'training_id': old.training_id.id,
            'registration_id': old.registration_id.id,
            'certificate_number': '%s-R%s' % (
                old.certificate_number,
                self.env['sf.employee.certification'].search_count([
                    ('employee_id', '=', old.employee_id.id),
                    ('training_id', '=', old.training_id.id),
                ]) + 1),
            'issue_date': self.new_issue_date,
            'expiration_date': self.new_expiration_date,
            'state': 'active',
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sf.employee.certification',
            'res_id': new_cert.id,
            'view_mode': 'form',
        }