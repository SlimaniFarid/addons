# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HaccpSite(models.Model):
    _name = 'sf.haccp.site'
    _description = 'HACCP Site'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    address = fields.Char(string='Address')
    manager_id = fields.Many2one('hr.employee', string='Manager',
                                 ondelete='restrict')
    active = fields.Boolean(string='Active', default=True)
    plan_ids = fields.One2many('sf.haccp.plan', 'site_id', string='Plans')
    prerequisite_ids = fields.One2many('sf.haccp.prerequisite', 'site_id',
                                       string='Prerequisites')
    check_ids = fields.One2many('sf.haccp.check', 'site_id',
                                string='Checks')
    nonconformity_ids = fields.One2many('sf.haccp.nonconformity', 'site_id',
                                        string='Nonconformities')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.haccp.site')
        return super().create(vals)


class HaccpPlan(models.Model):
    _name = 'sf.haccp.plan'
    _description = 'HACCP Plan'
    _order = 'site_id, name'

    name = fields.Char(string='Number', required=True, index=True)
    site_id = fields.Many2one('sf.haccp.site', string='Site', required=True,
                              ondelete='cascade', index=True)
    process = fields.Char(string='Process / Zone', required=True)
    version = fields.Integer(string='Version', default=1, required=True)
    scope = fields.Html(string='Scope')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    step_ids = fields.One2many('sf.haccp.step', 'plan_id', string='Steps')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.haccp.plan')
        return super().create(vals)

    def action_activate(self):
        self.ensure_one()
        if self.state not in ('draft', 'archived'):
            raise UserError(_('Only draft or archived plans can be '
                              'activated.'))
        self.state = 'active'

    def action_archive(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active plans can be archived.'))
        self.state = 'archived'


class HaccpStep(models.Model):
    _name = 'sf.haccp.step'
    _description = 'HACCP Plan Step'
    _order = 'plan_id, sequence'

    plan_id = fields.Many2one('sf.haccp.plan', string='Plan', required=True,
                              ondelete='cascade', index=True)
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    hazard = fields.Char(string='Hazard')
    is_ccp = fields.Boolean(string='CCP')
    critical_limit = fields.Char(string='Critical limit')
    monitoring = fields.Char(string='Monitoring')
    corrective = fields.Char(string='Corrective action')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='plan_id.company_id', store=True,
                                 readonly=True)


class HaccpPrerequisite(models.Model):
    _name = 'sf.haccp.prerequisite'
    _description = 'HACCP Prerequisite'
    _order = 'site_id, name'

    name = fields.Char(string='Number', required=True, index=True)
    site_id = fields.Many2one('sf.haccp.site', string='Site', required=True,
                              ondelete='cascade', index=True)
    category = fields.Selection([
        ('cleaning', 'Cleaning'),
        ('water', 'Water'),
        ('pest', 'Pest Control'),
        ('training', 'Training'),
        ('waste', 'Waste'),
        ('storage', 'Storage'),
        ('other', 'Other'),
    ], string='Category', default='cleaning', required=True)
    description = fields.Text(string='Description', required=True)
    status = fields.Selection([
        ('ok', 'OK'),
        ('fail', 'Fail'),
    ], string='Status', default='ok', required=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.haccp.prerequisite')
        return super().create(vals)


class HaccpCheck(models.Model):
    _name = 'sf.haccp.check'
    _description = 'HACCP Monitoring Check'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    site_id = fields.Many2one('sf.haccp.site', string='Site', required=True,
                              ondelete='cascade', index=True)
    plan_id = fields.Many2one('sf.haccp.plan', string='HACCP Plan',
                              ondelete='restrict')
    check_type = fields.Selection([
        ('temperature', 'Temperature'),
        ('cleaning', 'Cleaning'),
        ('ph', 'pH'),
        ('other', 'Other'),
    ], string='Type', default='temperature', required=True)
    target_min = fields.Float(string='Target min')
    target_max = fields.Float(string='Target max')
    unit = fields.Char(string='Unit')
    result = fields.Float(string='Result')
    control_date = fields.Datetime(string='Control date')
    operator_id = fields.Many2one('hr.employee', string='Operator',
                                  ondelete='restrict')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('done', 'Done'),
        ('deviated', 'Deviated'),
        ('resolved', 'Resolved'),
    ], string='Status', default='scheduled', required=True, tracking=True,
       index=True)
    deviation_detail = fields.Text(string='Deviation detail')
    nonconformity_ids = fields.One2many('sf.haccp.nonconformity',
                                        'check_id',
                                        string='Nonconformities')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.haccp.check')
        return super().create(vals)

    def action_validate(self):
        self.ensure_one()
        if self.state != 'scheduled':
            raise UserError(_('Only scheduled checks can be validated.'))
        if self.result is False or self.result is None:
            raise UserError(_('Record a result before validating the '
                              'check.'))
        out_of_range = False
        if self.target_min is not False and self.result < self.target_min:
            out_of_range = True
        if self.target_max is not False and self.result > self.target_max:
            out_of_range = True
        if out_of_range:
            detail = _('Result %s is outside the critical range [%s - %s] '
                       '%s.') % (self.result, self.target_min or '',
                                 self.target_max or '', self.unit or '')
            self.write({
                'state': 'deviated',
                'deviation_detail': detail,
            })
            self.env['sf.haccp.nonconformity'].create({
                'check_id': self.id,
                'site_id': self.site_id.id,
                'description': detail,
                'severity': 'major',
                'state': 'open',
                'company_id': self.company_id.id,
            })
        else:
            self.state = 'done'

    def action_resolve(self):
        self.ensure_one()
        if self.state != 'deviated':
            raise UserError(_('Only deviated checks can be resolved.'))
        open_nc = self.nonconformity_ids.filtered(
            lambda nc: nc.state != 'closed')
        if open_nc:
            raise UserError(_('Close all related nonconformities before '
                              'resolving the check.'))
        self.state = 'resolved'

    def _check_haccp_controls(self):
        companies = self.env['res.company'].search([])
        manager = self.env.ref('sf_haccp.group_haccp_manager')
        today = fields.Date.today()
        now = fields.Datetime.now()
        for company in companies:
            user = manager.users[:1] if manager.users else self.env.user
            checks = self.with_company(company).search([
                ('state', '=', 'scheduled'),
                ('control_date', '!=', False),
                ('result', '=', False),
                ('company_id', '=', company.id),
            ])
            for check in checks:
                margin = company.sf_haccp_alert_days or 0
                due = check.control_date + timedelta(days=margin)
                if now <= due:
                    continue
                existing = check.activity_ids.filtered(
                    lambda a: a.activity_type_id ==
                    self.env.ref('mail.mail_activity_data_todo')
                    and a.state != 'done')
                if existing:
                    continue
                check.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Scheduled HACCP check without result: %s')
                    % check.name,
                    user_id=user.id)
            ncs = self.env['sf.haccp.nonconformity'].with_company(
                company).search([
                    ('state', 'in', ['open', 'corrective_action']),
                    ('due_date', '!=', False),
                    ('due_date', '<', today),
                    ('company_id', '=', company.id),
                ])
            for nc in ncs:
                existing = nc.activity_ids.filtered(
                    lambda a: a.activity_type_id ==
                    self.env.ref('mail.mail_activity_data_todo')
                    and a.state != 'done')
                if existing:
                    continue
                nc.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Nonconformity %s is overdue') % nc.name,
                    user_id=user.id)


class HaccpNonconformity(models.Model):
    _name = 'sf.haccp.nonconformity'
    _description = 'HACCP Nonconformity'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    check_id = fields.Many2one('sf.haccp.check', string='Check',
                               ondelete='cascade', index=True)
    site_id = fields.Many2one('sf.haccp.site', string='Site', required=True,
                              ondelete='cascade', index=True)
    description = fields.Text(string='Description', required=True)
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ], string='Severity', default='minor', required=True)
    corrective_action = fields.Text(string='Corrective action')
    due_date = fields.Date(string='Due date', index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('corrective_action', 'Corrective Action'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    closed_date = fields.Datetime(string='Closed on')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.haccp.nonconformity')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_haccp.group_haccp_manager'):
            raise UserError(_('Only HACCP managers can close '
                              'nonconformities.'))

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft nonconformities can be opened.'))
        self.state = 'open'

    def action_start_corrective(self):
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('Only open nonconformities can move to '
                              'corrective action.'))
        if not self.corrective_action:
            raise UserError(_('Describe the corrective action before '
                              'moving to corrective action.'))
        self.state = 'corrective_action'

    def action_close(self):
        self.ensure_one()
        self._check_manager()
        if self.state not in ('open', 'corrective_action'):
            raise UserError(_('Only open nonconformities can be closed.'))
        if not self.corrective_action:
            raise UserError(_('A corrective action is required before '
                              'closing the nonconformity.'))
        if self.due_date and fields.Date.today() > self.due_date:
            raise UserError(_('The due date has passed; the nonconformity '
                              'cannot be closed.'))
        self.write({
            'state': 'closed',
            'closed_date': fields.Datetime.now(),
        })
        if self.check_id and self.check_id.state == 'deviated':
            open_nc = self.check_id.nonconformity_ids.filtered(
                lambda nc: nc.id != self.id and nc.state != 'closed')
            if not open_nc:
                self.check_id.state = 'resolved'