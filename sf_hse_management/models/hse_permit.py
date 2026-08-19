# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HsePermit(models.Model):
    _name = 'sf.hse.permit'
    _description = 'HSE Work Permit'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'start_date desc'

    name = fields.Char(string='Number', required=True,
                       default=lambda self: _('New'))
    permit_type = fields.Selection([
        ('fire', 'Fire Work'),
        ('confined_space', 'Confined Space'),
        ('height', 'Work at Height'),
        ('hot_work', 'Hot Work'),
        ('excavation', 'Excavation'),
        ('other', 'Other'),
    ], string='Type', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    location = fields.Char(string='Location', required=True)
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    description = fields.Text(string='Description')
    approved_by = fields.Many2one('res.users', string='Approved By')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for permit in self:
            if permit.end_date and permit.start_date:
                if permit.end_date < permit.start_date:
                    raise UserError(
                        _('The end date must be after the start date.'))

    def action_submit(self):
        for permit in self:
            if permit.state != 'draft':
                raise UserError(_('Only draft permits can be submitted.'))
            permit.state = 'submitted'
            permit.message_post(body=_('Permit submitted for approval.'))

    def action_approve(self):
        if not self.env.user.has_group(
                'sf_hse_management.group_hse_manager'):
            raise UserError(_('Only HSE managers can approve permits.'))
        for permit in self:
            if permit.state != 'submitted':
                raise UserError(
                    _('Only submitted permits can be approved.'))
            permit.state = 'approved'
            permit.approved_by = self.env.user
            permit.message_post(body=_('Permit approved.'))

    def action_start(self):
        for permit in self:
            if permit.state != 'approved':
                raise UserError(
                    _('Only approved permits can be started.'))
            permit.state = 'in_progress'
            permit.message_post(body=_('Permit work started.'))

    def action_reject(self):
        for permit in self:
            if permit.state != 'submitted':
                raise UserError(
                    _('Only submitted permits can be rejected.'))
            permit.state = 'rejected'
            permit.message_post(body=_('Permit rejected.'))

    def action_close(self):
        for permit in self:
            if permit.state not in ('in_progress', 'approved'):
                raise UserError(
                    _('Only in-progress or approved permits can be '
                      'closed.'))
            permit.state = 'closed'
            permit.message_post(body=_('Permit closed.'))

    def unlink(self):
        for permit in self:
            if permit.state in ('approved', 'in_progress'):
                raise UserError(
                    _('An active permit cannot be deleted.'))
        return super().unlink()