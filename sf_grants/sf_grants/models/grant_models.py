# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class GrantProgram(models.Model):
    _name = 'sf.grant.program'
    _description = 'Grant Program'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    funder = fields.Char(string='Funder', required=True)
    funder_type = fields.Selection([
        ('european', 'European'),
        ('state', 'State'),
        ('regional', 'Regional'),
        ('private', 'Private'),
        ('other', 'Other'),
    ], string='Funder type', required=True)
    description = fields.Text(string='Description')
    call_ids = fields.One2many('sf.grant.call', 'program_id',
                               string='Calls for projects')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.grant.program')
        return super().create(vals)


class GrantCall(models.Model):
    _name = 'sf.grant.call'
    _description = 'Grant Call for Projects'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    program_id = fields.Many2one('sf.grant.program', string='Program',
                                 required=True, ondelete='cascade',
                                 index=True)
    title = fields.Char(string='Title', required=True)
    budget = fields.Float(string='Budget')
    open_date = fields.Date(string='Opening date')
    deadline_date = fields.Date(string='Deadline date')
    max_amount = fields.Float(string='Maximum amount per application')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    application_ids = fields.One2many('sf.grant.application', 'call_id',
                                      string='Applications')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.grant.call')
        return super().create(vals)

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft calls can be opened.'))
        self.state = 'open'

    def action_close_call(self):
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('Only open calls can be closed.'))
        self.state = 'closed'

    def _check_manager(self):
        if not self.env.user.has_group('sf_grants.group_grant_manager'):
            raise UserError(_('Only grant managers can perform this '
                              'operation.'))

    @api.model
    def _check_grant_alerts(self):
        today = fields.Date.today()
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            alert_days = company.sf_grant_alert_days or 0
            calls = self.with_company(company).search([
                ('state', '=', 'open'),
                ('company_id', '=', company.id),
                ('deadline_date', '!=', False),
            ])
            for call in calls:
                if (call.deadline_date
                        - timedelta(days=alert_days)) > today:
                    continue
                if call.application_ids.filtered(
                        lambda a: a.state != 'draft'):
                    continue
                existing = call.activity_ids.filtered(
                    lambda a: a.activity_type_id == todo_type
                    and a.state != 'done')
                if existing:
                    continue
                call.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Grant call deadline approaching: %s')
                    % call.name,
                    date_deadline=call.deadline_date,
                    user_id=self.env.user.id)
            applications = self.env['sf.grant.application'].with_company(
                company).search([
                ('state', 'in', ('approved', 'paid', 'closed')),
                ('company_id', '=', company.id),
                ('granted_amount', '>', 0),
            ])
            for application in applications:
                if application.expense_ids.filtered(
                        lambda e: e.state == 'validated'):
                    continue
                existing = application.activity_ids.filtered(
                    lambda a: a.activity_type_id == todo_type
                    and a.state != 'done')
                if existing:
                    continue
                application.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Expense reporting expected for grant: %s')
                    % application.name,
                    user_id=self.env.user.id)


class GrantApplication(models.Model):
    _name = 'sf.grant.application'
    _description = 'Grant Application'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    call_id = fields.Many2one('sf.grant.call', string='Call for projects',
                              ondelete='restrict', index=True)
    program_id = fields.Many2one('sf.grant.program', string='Program',
                                 related='call_id.program_id', store=True,
                                 readonly=True)
    funder_type = fields.Selection([
        ('european', 'European'),
        ('state', 'State'),
        ('regional', 'Regional'),
        ('private', 'Private'),
        ('other', 'Other'),
    ], string='Funder type', related='call_id.program_id.funder_type',
       store=True, readonly=True)
    title = fields.Char(string='Title', required=True)
    applicant = fields.Char(string='Applicant', required=True)
    requested_amount = fields.Float(string='Requested amount')
    granted_amount = fields.Float(string='Granted amount')
    currency = fields.Char(string='Currency', default='EUR', required=True)
    submission_date = fields.Date(string='Submission date')
    decision_date = fields.Date(string='Decision date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    expense_ids = fields.One2many('sf.grant.expense', 'application_id',
                                  string='Expenses')
    total_validated_amount = fields.Float(
        string='Total validated expenses',
        compute='_compute_total_validated_amount', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('expense_ids.amount', 'expense_ids.state')
    def _compute_total_validated_amount(self):
        for application in self:
            application.total_validated_amount = sum(
                application.expense_ids.filtered(
                    lambda e: e.state == 'validated').mapped('amount'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.grant.application')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_grants.group_grant_manager'):
            raise UserError(_('Only grant managers can perform this '
                              'operation.'))

    def action_submit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft applications can be submitted.'))
        if not self.call_id:
            raise UserError(_('An application must reference a call for '
                              'projects before submission.'))
        if not self.requested_amount:
            raise UserError(_('A requested amount is required before '
                              'submission.'))
        self.write({
            'submission_date': fields.Date.today(),
            'state': 'submitted',
        })

    def action_approve(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'submitted':
            raise UserError(_('Only submitted applications can be '
                              'approved.'))
        self.write({
            'granted_amount': self.requested_amount
            if not self.granted_amount else self.granted_amount,
            'decision_date': fields.Date.today(),
            'state': 'approved',
        })

    def action_pay(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'approved':
            raise UserError(_('Only approved applications can be paid.'))
        self.state = 'paid'

    def action_close(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'paid':
            raise UserError(_('Only paid applications can be closed.'))
        self.state = 'closed'

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'submitted':
            raise UserError(_('Only submitted applications can be '
                              'rejected.'))
        self.write({
            'decision_date': fields.Date.today(),
            'state': 'rejected',
        })


class GrantExpense(models.Model):
    _name = 'sf.grant.expense'
    _description = 'Grant Expense'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    application_id = fields.Many2one('sf.grant.application',
                                     string='Application', required=True,
                                     ondelete='cascade', index=True)
    expense_date = fields.Date(string='Expense date')
    category = fields.Selection([
        ('personnel', 'Personnel'),
        ('equipment', 'Equipment'),
        ('travel', 'Travel'),
        ('consulting', 'Consulting'),
        ('other', 'Other'),
    ], string='Category', required=True)
    amount = fields.Float(string='Amount', required=True)
    justification = fields.Char(string='Justification',
                                help='Invoice or supporting document '
                                'number')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('claimed', 'Claimed'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', required=True, index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.grant.expense')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_grants.group_grant_manager'):
            raise UserError(_('Only grant managers can perform this '
                              'operation.'))

    def action_claim(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft expenses can be claimed.'))
        self.state = 'claimed'

    def action_validate(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'claimed':
            raise UserError(_('Only claimed expenses can be validated.'))
        if not self.justification:
            raise UserError(_('A justification is required to validate an '
                              'expense.'))
        total = sum(self.application_id.expense_ids.filtered(
            lambda e: e.state == 'validated').mapped('amount')) \
            + self.amount
        if total > (self.application_id.granted_amount or 0.0):
            raise UserError(_('The validated expenses would exceed the '
                              'granted amount of %s.')
                            % self.application_id.granted_amount)
        self.state = 'validated'

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'claimed':
            raise UserError(_('Only claimed expenses can be rejected.'))
        self.state = 'rejected'