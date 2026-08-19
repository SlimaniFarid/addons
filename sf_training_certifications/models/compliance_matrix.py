# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ComplianceMatrix(models.Model):
    _name = 'sf.compliance.matrix'
    _description = 'Training Compliance Matrix'
    _order = 'employee_id, training_id'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    training_id = fields.Many2one('sf.training', string='Training',
                                  required=True)
    category_id = fields.Many2one('sf.training.category',
                                  string='Category',
                                  related='training_id.category_id',
                                  store=True)
    certification_id = fields.Many2one('sf.employee.certification',
                                       string='Certification')
    cert_state = fields.Selection([
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
        ('none', 'Not Certified'),
    ], string='Certification Status', compute='_compute_cert_state',
       store=True)
    compliant = fields.Boolean(string='Compliant',
                               compute='_compute_cert_state', store=True)

    @api.depends('certification_id.state', 'training_id.mandatory')
    def _compute_cert_state(self):
        for row in self:
            cert = row.certification_id
            if not cert:
                row.cert_state = 'none'
                row.compliant = False
            elif cert.state == 'active':
                row.cert_state = 'active'
                row.compliant = True
            elif cert.state == 'expiring':
                row.cert_state = 'expiring'
                row.compliant = True
            else:
                row.cert_state = cert.state
                row.compliant = False

    @api.model
    def _refresh_matrix(self):
        trainings = self.env['sf.training'].search([
            ('mandatory', '=', True),
        ])
        employees = self.env['hr.employee'].search([])
        self.search([]).unlink()
        rows = self.env['sf.compliance.matrix']
        for employee in employees:
            for training in trainings:
                cert = self.env['sf.employee.certification'].search([
                    ('employee_id', '=', employee.id),
                    ('training_id', '=', training.id),
                    ('state', '!=', 'renewed'),
                ], order='issue_date desc', limit=1)
                rows.create({
                    'employee_id': employee.id,
                    'training_id': training.id,
                    'certification_id': cert.id if cert else False,
                })
        return True