# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HseIncident(models.Model):
    _name = 'sf.hse.incident'
    _description = 'HSE Incident'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'incident_date desc'

    name = fields.Char(string='Number', required=True,
                       default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee')
    incident_type = fields.Selection([
        ('accident', 'Accident'),
        ('near_miss', 'Near Miss'),
        ('property_damage', 'Property Damage'),
        ('environmental', 'Environmental'),
        ('other', 'Other'),
    ], string='Type', required=True, tracking=True)
    incident_date = fields.Datetime(string='Date', required=True)
    location = fields.Char(string='Location')
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ], string='Severity', required=True, default='minor', tracking=True)
    description = fields.Text(string='Description', required=True)
    root_cause = fields.Text(string='Root Cause')
    investigation_report = fields.Html(string='Investigation Report')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reported', 'Reported'),
        ('under_investigation', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    reported_by = fields.Many2one('res.users', string='Reported By',
                                  default=lambda self: self.env.user)
    actions = fields.One2many('sf.hse.incident.action', 'incident_id',
                              string='Corrective Actions')
    attachment_ids = fields.Many2many(
        'ir.attachment', string='Attachments')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    days_without_accident = fields.Integer(
        string='Days Without Accident', compute='_compute_days_without',
        store=False)

    @api.depends('company_id.sf_hse_last_major_incident')
    def _compute_days_without(self):
        today = fields.Date.today()
        for incident in self:
            last = incident.company_id.sf_hse_last_major_incident
            if not last:
                incident.days_without_accident = 0
                continue
            last_date = fields.Datetime.from_string(last).date()
            incident.days_without_accident = max((today - last_date).days, 0)

    @api.constrains('incident_type', 'severity', 'description')
    def _check_incident(self):
        for incident in self:
            if not incident.description:
                raise UserError(_('A description is required for an '
                                  'incident.'))

    def action_report(self):
        for incident in self:
            if incident.state != 'draft':
                raise UserError(_('Only draft incidents can be reported.'))
            incident.state = 'reported'
            if incident.severity in ('major', 'critical'):
                incident.company_id.sf_hse_last_major_incident = \
                    fields.Datetime.now()
            incident.message_post(body=_('Incident reported.'))

    def action_start_investigation(self):
        for incident in self:
            if incident.state != 'reported':
                raise UserError(
                    _('Only reported incidents can be investigated.'))
            incident.state = 'under_investigation'
            incident.message_post(body=_('Investigation started.'))

    def action_resolve(self):
        for incident in self:
            if incident.state != 'under_investigation':
                raise UserError(
                    _('Only incidents under investigation can be resolved.'))
            open_actions = incident.actions.filtered(
                lambda a: a.state == 'open')
            if open_actions:
                raise UserError(
                    _('All corrective actions must be completed before '
                      'resolving the incident.'))
            incident.state = 'resolved'
            incident.message_post(body=_('Incident resolved.'))

    def action_reject(self):
        for incident in self:
            if incident.state not in ('reported', 'under_investigation'):
                raise UserError(
                    _('Only reported or investigated incidents can be '
                      'rejected.'))
            incident.state = 'rejected'
            incident.message_post(body=_('Incident rejected.'))

    def action_close(self):
        for incident in self:
            if incident.state not in ('resolved', 'rejected'):
                raise UserError(
                    _('Only resolved or rejected incidents can be closed.'))
            incident.state = 'closed'
            incident.message_post(body=_('Incident closed.'))

    def unlink(self):
        for incident in self:
            if incident.state in ('reported', 'under_investigation',
                                  'resolved'):
                raise UserError(
                    _('An active incident cannot be deleted.'))
        return super().unlink()


class HseIncidentAction(models.Model):
    _name = 'sf.hse.incident.action'
    _description = 'HSE Incident Corrective Action'
    _order = 'due_date'

    incident_id = fields.Many2one('sf.hse.incident', string='Incident',
                                  ondelete='cascade', required=True)
    action_type = fields.Selection([
        ('corrective', 'Corrective'),
        ('preventive', 'Preventive'),
    ], string='Type', default='corrective', required=True)
    description = fields.Text(string='Description', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible',
                                     required=True)
    due_date = fields.Date(string='Due Date', required=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='open', tracking=True)
    completion_note = fields.Text(string='Completion Note')
    closed_date = fields.Datetime(string='Closed Date')

    @api.constrains('due_date')
    def _check_due_date(self):
        for action in self:
            if action.due_date and action.create_date:
                from datetime import datetime
                create = action.create_date.date()
                if action.due_date < create:
                    raise UserError(
                        _('The due date cannot be before the creation '
                          'date.'))

    def action_done(self):
        for action in self:
            if action.state != 'open':
                raise UserError(_('Only open actions can be completed.'))
            if not action.completion_note:
                raise UserError(_('A completion note is required to '
                                  'complete the action.'))
            action.state = 'done'
            action.closed_date = fields.Datetime.now()
            action.incident_id.message_post(body=_(
                'Action "%s" completed.') % action.description)

    def action_cancel(self):
        for action in self:
            if action.state != 'open':
                raise UserError(_('Only open actions can be cancelled.'))
            action.state = 'cancelled'