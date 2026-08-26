# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCleaningSchedule(models.Model):
    _name = 'sf.cleaning.schedule'
    _description = 'Cleaning Schedule'
    _order = 'planned_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)
    contract_id = fields.Many2one(
        'sf.cleaning.contract', string='Contract', ondelete='restrict',
        required=True, index=True, tracking=True)
    site_id = fields.Many2one(
        'sf.cleaning.site', string='Site', ondelete='restrict',
        required=True, index=True, tracking=True)
    agent_id = fields.Many2one(
        'res.users', string='Agent', tracking=True)
    planned_date = fields.Date(
        string='Planned date', required=True, tracking=True, index=True)
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In progress'),
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
        ('invoiced', 'Invoiced'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', required=True, tracking=True,
       index=True)
    qty = fields.Float(string='Quantity', default=1.0, tracking=True)
    line_ids = fields.One2many(
        'sf.cleaning.schedule.line', 'schedule_id', string='Interventions')
    invoice_amount = fields.Float(
        string='Invoice amount', compute='_compute_invoice_amount', store=True)
    activity_date = fields.Date(string='Alert activity date')

    @api.depends('qty', 'contract_id.line_ids.unit_price',
                 'contract_id.line_ids.site_id', 'site_id')
    def _compute_invoice_amount(self):
        for schedule in self:
            line = schedule.contract_id.line_ids.filtered(
                lambda l: l.site_id == schedule.site_id)[:1]
            schedule.invoice_amount = schedule.qty * (
                line.unit_price if line else 0.0)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.cleaning.schedule')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_cleaning.group_sf_cleaning_manager'):
            raise UserError(_('Only managers can perform this action.'))

    def unlink(self):
        self._check_manager()
        return super().unlink()

    def action_start(self):
        for schedule in self:
            if schedule.state != 'planned':
                raise UserError(_('Only planned schedules can be started.'))
        self.state = 'in_progress'

    def action_submit(self):
        for schedule in self:
            if schedule.state != 'in_progress':
                raise UserError(_('Only in progress schedules can be '
                                  'submitted.'))
        self.state = 'submitted'

    def action_validate(self):
        self._check_manager()
        for schedule in self:
            if schedule.state != 'submitted':
                raise UserError(_('Only submitted schedules can be '
                                  'validated.'))
            for line in schedule.line_ids.filtered(
                    lambda l: l.state == 'done'):
                if not line.quality_check_id:
                    raise UserError(_('An intervention cannot be validated '
                                      'without a quality check.'))
        self.state = 'validated'

    def action_invoice(self):
        self._check_manager()
        for schedule in self:
            if schedule.state != 'validated':
                raise UserError(_('Only validated schedules can be '
                                  'invoiced.'))
            if not schedule.line_ids.filtered(lambda l: l.state == 'done'):
                raise UserError(_('Invoicing is blocked until validated '
                                  'interventions are selected.'))
        self.state = 'invoiced'

    def action_cancel(self):
        self._check_manager()
        for schedule in self:
            if schedule.state not in ('planned', 'in_progress', 'submitted'):
                raise UserError(_('Only planned, in progress or submitted '
                                  'schedules can be cancelled.'))
        self.state = 'cancelled'

    @api.model
    def _cron_sf_cleaning_alert(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        for company in self.env['res.company'].search([]):
            if not company.sf_cleaning_alert_enabled:
                continue
            today = fields.Date.context_today(self.with_company(company))
            threshold = today - timedelta(
                days=company.sf_cleaning_overdue_days)
            schedules = self.with_company(company).search([
                ('state', 'in', ['planned', 'in_progress', 'submitted']),
                ('planned_date', '!=', False),
            ])
            for schedule in schedules:
                overdue = schedule.planned_date < threshold
                unassigned = not schedule.agent_id
                if not (overdue or unassigned):
                    continue
                existing = self.env['mail.activity'].search([
                    ('res_model', '=', schedule._name),
                    ('res_id', '=', schedule.id),
                    ('activity_type_id', '=', todo_type.id),
                    ('user_id', '=', self.env.user.id),
                ], limit=1)
                if existing:
                    continue
                if schedule.activity_ids.filtered(
                        lambda a: a.activity_type_id == todo_type):
                    continue
                schedule.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('SF Cleaning alert: %s') % schedule.name,
                    user_id=self.env.user.id)
                schedule.activity_date = today