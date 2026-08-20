# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfPolicy(models.Model):
    _name = 'sf.policy'
    _description = 'Company Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.policy.activity.mixin']
    _order = 'effective_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    policy_type = fields.Selection([
        ('general', 'General'),
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('it', 'Information Technology'),
        ('compliance', 'Compliance'),
    ], string='Category', default='general', required=True)
    version = fields.Char(string='Version', default='1.0', required=True)
    effective_date = fields.Date(string='Effective Date', required=True)
    expiry_date = fields.Date(string='Expiry Date')
    owner_id = fields.Many2one(
        'res.users', string='Owner', default=lambda self: self.env.user)
    body = fields.Html(string='Content')
    employee_ids = fields.Many2many(
        'hr.employee', string='Assigned Employees')
    acknowledgment_ids = fields.One2many(
        'sf.policy.acknowledgment', 'policy_id', string='Acknowledgment Register')
    acknowledgment_rate = fields.Float(
        string='Acknowledgment Rate (%)', compute='_compute_acknowledgment_rate',
        store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('retired', 'Retired'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    @api.depends('acknowledgment_ids.state')
    def _compute_acknowledgment_rate(self):
        for policy in self:
            total = len(policy.acknowledgment_ids)
            acknowledged = len(
                policy.acknowledgment_ids.filtered(
                    lambda a: a.state == 'acknowledged'))
            policy.acknowledgment_rate = \
                (acknowledged * 100.0 / total) if total else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.policy')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_policy_acknowledgment.group_sf_policy_manager'):
            raise UserError(_('Only a policy manager can perform this action.'))

    def _set_state(self, state):
        self.ensure_one()
        self.with_context(sf_policy_bypass_state=True).write(
            {'state': state})

    def write(self, vals):
        if 'state' in vals and not self.env.context.get(
                'sf_policy_bypass_state'):
            raise UserError(_('The status cannot be modified directly.'))
        locked = self.filtered(lambda p: p.state != 'draft')
        locked_fields = {'name', 'policy_type', 'version',
                         'effective_date', 'expiry_date', 'owner_id',
                         'body', 'employee_ids'}
        if locked and locked_fields & set(vals) \
                and not self.env.context.get('sf_policy_bypass_state'):
            raise UserError(_('Only draft policies can be modified.'))
        return super().write(vals)

    def action_publish(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'draft':
            raise UserError(_('Only draft policies can be published.'))
        self._set_state('published')
        for employee in self.employee_ids:
            existing = self.acknowledgment_ids.filtered(
                lambda a: a.employee_id == employee)
            if not existing:
                self.env['sf.policy.acknowledgment'].create({
                    'policy_id': self.id,
                    'employee_id': employee.id,
                    'company_id': self.company_id.id,
                })

    def action_retire(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'published':
            raise UserError(_('Only published policies can be retired.'))
        self._set_state('retired')

    def action_archive(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'retired':
            raise UserError(_('Only retired policies can be archived.'))
        self._set_state('archived')

    def _cron_ack_reminders(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            pending = scoped.env['sf.policy.acknowledgment'].search([
                ('state', '=', 'pending'),
                ('policy_id.state', '=', 'published'),
            ])
            for ack in pending:
                user = ack.employee_id.user_id or ack.policy_id.owner_id
                if user:
                    ack._sf_check_todo(
                        todo_type,
                        'Acknowledge policy: %s' % ack.policy_id.name,
                        'Please acknowledge the policy %s.' % ack.policy_id.name,
                        user_id=user.id,
                    )

    def _cron_expiry_reminders(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            param = self.env['ir.config_parameter'].sudo().get_param(
                'sf_policy_acknowledgment.expiry_reminder_days')
            reminder_days = int(param) if param else 30
            horizon = today + timedelta(days=reminder_days)
            expiring = scoped.env['sf.policy'].search([
                ('state', '=', 'published'),
                ('expiry_date', '>=', today),
                ('expiry_date', '<=', horizon),
            ])
            for policy in expiring:
                policy._sf_check_todo(
                    todo_type,
                    'Policy expiring: %s' % policy.name,
                    'The policy %s expires on %s.' % (
                        policy.name, policy.expiry_date),
                    user_id=policy.owner_id.id,
                )