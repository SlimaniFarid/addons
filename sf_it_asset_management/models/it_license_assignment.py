# -*- coding: utf-8 -*-
from odoo import fields, models, _, api
from odoo.exceptions import UserError


class ItLicenseAssignment(models.Model):
    _name = 'sf.it.license.assignment'
    _description = 'IT License Seat Assignment'
    _order = 'date_from desc'

    license_id = fields.Many2one('sf.it.license', string='License',
                                 required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    asset_id = fields.Many2one('sf.it.asset', string='Asset')
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To')
    state = fields.Selection([
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='active')

    @api.constrains('license_id', 'employee_id', 'state')
    def _check_unique_and_seats(self):
        for assignment in self:
            if assignment.state != 'active':
                continue
            if assignment.license_id.state == 'expired':
                raise UserError(
                    _('A seat cannot be assigned to an expired license.'))
            duplicate = self.env['sf.it.license.assignment'].search([
                ('license_id', '=', assignment.license_id.id),
                ('employee_id', '=', assignment.employee_id.id),
                ('state', '=', 'active'),
                ('id', '!=', assignment.id),
            ])
            if duplicate:
                raise UserError(
                    _('This employee already has an active seat on '
                      'this license.'))
            if not assignment.license_id.unlimited:
                used = sum(1 for a in
                           self.env['sf.it.license.assignment'].search([
                               ('license_id', '=',
                                assignment.license_id.id),
                               ('state', '=', 'active'),
                               ('id', '!=', assignment.id),
                           ]))
                if used >= assignment.license_id.seats:
                    raise UserError(
                        _('No available seat on this license.'))

    def action_close(self):
        for rec in self:
            rec.write({
                'state': 'closed',
                'date_to': rec.date_to or fields.Date.today(),
            })