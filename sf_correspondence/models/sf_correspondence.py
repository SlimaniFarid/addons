# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfCorrespondence(models.Model):
    _name = 'sf.correspondence'
    _description = 'Correspondence'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.correspondence.activity.mixin']
    _order = 'correspondence_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    direction = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ], string='Direction', required=True)
    correspondence_date = fields.Date(
        string='Date', default=fields.Date.context_today)
    partner_id = fields.Many2one(
        'res.partner', string='Correspondent', required=True)
    department_id = fields.Many2one(
        'sf.correspondence.department', string='Department')
    assigned_to = fields.Many2one(
        'res.users', string='Assigned To',
        default=lambda self: self.env.user)
    subject = fields.Char(string='Subject', required=True)
    reference = fields.Char(string='Reference')
    registered_mail = fields.Boolean(string='Registered Mail')
    ack_received = fields.Boolean(string='Acknowledgment Received')
    response_due_date = fields.Date(string='Response Due Date')
    response_date = fields.Date(string='Response Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('responded', 'Responded'),
        ('archived', 'Archived'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    attachment_ids = fields.One2many(
        'ir.attachment', 'res_id', string='Attachments',
        domain=lambda self: [('res_model', '=', self._name)])
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.correspondence')
            if not vals.get('assigned_to'):
                vals['assigned_to'] = self.env.user.id
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_correspondence.group_sf_correspondence_manager'):
            raise UserError(_('Only a correspondence manager can perform this action.'))

    def _set_state(self, state):
        self.ensure_one()
        self.with_context(sf_correspondence_bypass_state=True).write(
            {'state': state})

    def write(self, vals):
        if 'state' in vals and not self.env.context.get(
                'sf_correspondence_bypass_state'):
            raise UserError(_('The status cannot be modified directly.'))
        return super().write(vals)

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft correspondence can be opened.'))
        self._set_state('open')

    def action_start(self):
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('Only open correspondence can be put in progress.'))
        self._set_state('in_progress')

    def action_responded(self):
        self.ensure_one()
        if self.state not in ('open', 'in_progress'):
            raise UserError(_('Only open or in-progress correspondence can be marked as responded.'))
        if not self.response_date:
            self.response_date = fields.Date.context_today(self)
        self._set_state('responded')

    def action_archive(self):
        self.ensure_one()
        if self.state != 'responded':
            raise UserError(_('Only responded correspondence can be archived.'))
        self._set_state('archived')

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('responded', 'archived', 'cancelled'):
            raise UserError(_('A responded, archived or cancelled correspondence cannot be cancelled.'))
        self._set_state('cancelled')

    def _cron_followups(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            param = self.env['ir.config_parameter'].sudo().get_param(
                'sf_correspondence.default_reminder_days')
            reminder_days = int(param) if param else 2
            deadline = today + timedelta(days=reminder_days)
            due = scoped.env['sf.correspondence'].search([
                ('state', 'in', ('open', 'in_progress')),
                ('response_due_date', '!=', False),
                ('response_due_date', '<=', deadline),
            ])
            for record in due:
                record._sf_check_todo(
                    todo_type,
                    'Response due for %s' % record.name,
                    'The response is due since %s.' % record.response_due_date,
                )