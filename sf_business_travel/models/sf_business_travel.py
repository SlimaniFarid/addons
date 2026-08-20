# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfBusinessTravel(models.Model):
    _name = 'sf.business.travel'
    _description = 'Business Travel'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.business.travel.activity.mixin']
    _order = 'departure_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    employee_id = fields.Many2one(
        'res.users', string='Employee',
        default=lambda self: self.env.user, required=True)
    purpose = fields.Char(string='Purpose', required=True)
    destination = fields.Char(string='Destination', required=True)
    departure_date = fields.Date(string='Departure Date', required=True)
    return_date = fields.Date(string='Return Date', required=True)
    budget = fields.Monetary(string='Budget', currency_field='currency_id')
    estimated_cost = fields.Monetary(
        string='Estimated Cost', compute='_compute_estimated_cost',
        store=True, currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        related='company_id.currency_id', readonly=True, store=True)
    justification = fields.Text(string='Justification')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    line_ids = fields.One2many(
        'sf.business.travel.line', 'travel_id', string='Itinerary')
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_return_after_departure',
         'CHECK (return_date >= departure_date)',
         'The return date cannot be before the departure date.'),
    ]

    _EDITABLE_STATES = ('draft', 'submitted', 'rejected')
    _EDITABLE_FIELDS = {
        'employee_id', 'purpose', 'destination', 'departure_date',
        'return_date', 'budget', 'justification',
    }

    @api.depends('line_ids.amount')
    def _compute_estimated_cost(self):
        for travel in self:
            travel.estimated_cost = sum(
                travel.line_ids.mapped('amount') or [0.0])

    @api.constrains('departure_date', 'return_date')
    def _check_dates(self):
        for travel in self:
            if travel.return_date and travel.departure_date and \
                    travel.return_date < travel.departure_date:
                raise ValidationError(_('The return date cannot be before the departure date.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.business.travel')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_business_travel.group_sf_business_travel_manager'):
            raise UserError(_('Only a travel manager can perform this action.'))

    def _set_state(self, state):
        self.ensure_one()
        self.with_context(sf_business_travel_bypass_state=True).write(
            {'state': state})

    def write(self, vals):
        if 'state' in vals and not self.env.context.get(
                'sf_business_travel_bypass_state'):
            raise UserError(_('The status cannot be modified directly.'))
        blocked = self.filtered(
            lambda t: t.state not in self._EDITABLE_STATES)
        if blocked and self._EDITABLE_FIELDS & set(vals):
            raise UserError(_('An approved, in-progress, completed or cancelled travel cannot be modified.'))
        return super().write(vals)

    def action_submit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft travels can be submitted.'))
        if not self.destination or not self.departure_date or \
                not self.return_date or not self.purpose:
            raise UserError(_('Destination, dates and purpose are required before submission.'))
        self._set_state('submitted')

    def action_approve(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'submitted':
            raise UserError(_('Only submitted travels can be approved.'))
        self._set_state('approved')

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'submitted':
            raise UserError(_('Only submitted travels can be rejected.'))
        self._set_state('rejected')

    def action_start(self):
        self.ensure_one()
        if self.state != 'approved':
            raise UserError(_('Only approved travels can start.'))
        self._set_state('in_progress')

    def action_complete(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress travels can be completed.'))
        self._set_state('completed')

    def action_cancel(self):
        for record in self:
            if record.state in ('completed', 'cancelled'):
                raise UserError(_('A completed or cancelled travel cannot be cancelled.'))
            if not self.env.user.has_group(
                    'sf_business_travel.group_sf_business_travel_manager') \
                    and record.employee_id != self.env.user:
                raise UserError(_('Only the employee or a travel manager can cancel this travel.'))
        for record in self:
            record._set_state('cancelled')

    def _cron_departure_reminders(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            param = self.env['ir.config_parameter'].sudo().get_param(
                'sf_business_travel.reminder_days')
            reminder_days = int(param) if param else 2
            horizon = today + timedelta(days=reminder_days)
            upcoming = scoped.env['sf.business.travel'].search([
                ('state', 'in', ('approved', 'in_progress')),
                ('departure_date', '>=', today),
                ('departure_date', '<=', horizon),
            ])
            for travel in upcoming:
                travel._sf_check_todo(
                    todo_type,
                    'Departure reminder: %s' % travel.name,
                    'The travel departs on %s.' % travel.departure_date,
                )