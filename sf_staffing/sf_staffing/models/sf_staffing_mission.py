# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfStaffingMission(models.Model):
    _name = 'sf.staffing.mission'
    _description = 'Staffing Mission'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.staffing.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    client_id = fields.Many2one('sf.staffing.client', string='Client', required=True, ondelete='restrict')
    candidate_id = fields.Many2one('sf.staffing.candidate', string='Candidate', required=True, ondelete='restrict')
    need_id = fields.Many2one('sf.staffing.need', string='Need', ondelete='set null')
    contract_id = fields.Many2one('sf.staffing.contract', string='Contract', ondelete='set null', readonly=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    hourly_rate = fields.Monetary(string='Hourly Rate', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    timesheet_ids = fields.One2many('sf.staffing.timesheet', 'mission_id', string='Timesheets')
    invoice_ids = fields.One2many('account.move', 'sf_staffing_mission_id', string='Invoices')
    total_billable = fields.Monetary(
        string='Billable Amount',
        compute='_compute_total_billable',
        store=True,
        currency_field='currency_id',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('timesheet_ids.amount', 'timesheet_ids.state')
    def _compute_total_billable(self):
        for mission in self:
            mission.total_billable = sum(
                mission.timesheet_ids.filtered(lambda t: t.state == 'done').mapped('amount')
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.staffing.mission')
            if vals.get('start_date') and vals.get('end_date') and vals['end_date'] < vals['start_date']:
                raise UserError(_('The end date must be later than or equal to the start date.'))
        missions = super().create(vals_list)
        for mission in missions:
            if not mission.contract_id:
                mission._create_contract()
        return missions

    def _create_contract(self):
        self.ensure_one()
        contract = self.env['sf.staffing.contract'].create({
            'mission_id': self.id,
            'candidate_id': self.candidate_id.id,
            'client_id': self.client_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'hourly_rate': self.hourly_rate,
            'company_id': self.company_id.id,
        })
        self.contract_id = contract
        return contract

    def write(self, vals):
        if 'hourly_rate' in vals and any(mission.state != 'draft' for mission in self):
            self._check_manager()
        return super().write(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_staffing.group_sf_staffing_manager'):
            raise UserError(_('Only a staffing manager can perform this action.'))

    def _check_candidate_active_mission(self):
        self.ensure_one()
        active = self.env['sf.staffing.mission'].search([
            ('candidate_id', '=', self.candidate_id.id),
            ('state', 'in', ('confirmed', 'in_progress')),
            ('id', '!=', self.id),
        ])
        if active:
            raise UserError(_('Candidate already on a mission.'))

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft missions can be confirmed.'))
        self._check_candidate_active_mission()
        self.state = 'confirmed'
        self.contract_id.state = 'confirmed'
        self.candidate_id.state = 'on_mission'
        if self.need_id and self.need_id.state == 'open':
            self.need_id.state = 'assigned'

    def action_start(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed missions can be started.'))
        self._check_candidate_active_mission()
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'in_progress'):
            raise UserError(_('Only confirmed or in-progress missions can be marked as done.'))
        self.state = 'done'
        self.contract_id.state = 'done'
        self.candidate_id.state = 'available'
        if self.need_id and self.need_id.state in ('assigned', 'open'):
            self.need_id.state = 'filled'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_('A completed mission cannot be cancelled.'))
        if self.state in ('confirmed', 'in_progress'):
            self._check_manager()
        self.state = 'cancelled'
        self.contract_id.state = 'cancelled'
        if self.candidate_id.state == 'on_mission':
            self.candidate_id.state = 'available'
        if self.need_id and self.need_id.state in ('assigned', 'filled'):
            self.need_id.state = 'open'

    def action_create_invoice(self):
        self.ensure_one()
        done_timesheets = self.timesheet_ids.filtered(lambda t: t.state == 'done' and not t.invoiced)
        if not done_timesheets:
            raise UserError(_('No validated and non-invoiced timesheet to invoice.'))
        partner = self.client_id.partner_id
        if not partner:
            partner = self.env['res.partner'].create({'name': self.client_id.name})
            self.client_id.partner_id = partner
        journal = self.env['account.journal'].search([
            ('type', '=', 'sale'),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        if not journal:
            journal = self.env['account.journal'].search([
                ('type', '=', 'general'),
                ('company_id', '=', self.company_id.id),
            ], limit=1)
        if not journal:
            raise UserError(_('No sale or general journal found for the mission company.'))
        invoice = self.env['account.move'].with_company(self.company_id).create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'journal_id': journal.id,
            'company_id': self.company_id.id,
            'ref': self.name,
            'sf_staffing_mission_id': self.id,
            'invoice_line_ids': [
                (0, 0, {
                    'name': '%s - %s' % (self.name, timesheet.date),
                    'quantity': timesheet.hours,
                    'price_unit': timesheet.hourly_rate,
                })
                for timesheet in done_timesheets
            ],
        })
        done_timesheets.write({'invoiced': True})
        return {
            'name': _('Mission Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

    def action_validate_invoices(self):
        self._check_manager()
        invoices = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
        for invoice in invoices:
            invoice.action_post()
        return True

    def _cron_daily_alerts(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        reminder_days = int(self.env['ir.config_parameter'].sudo().get_param(
            'sf_staffing.mission_end_reminder_days', '7'
        ))
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            limit_date = today + timedelta(days=reminder_days)
            missions = scoped.env['sf.staffing.mission'].search([
                ('state', 'in', ('confirmed', 'in_progress')),
                ('end_date', '<=', limit_date),
                ('end_date', '>=', today),
            ])
            for mission in missions:
                mission._sf_check_todo(
                    todo_type,
                    'Mission %s ends on %s' % (mission.name, mission.end_date),
                    'Reminder: this mission reaches its end date within %s days.' % reminder_days,
                )
            yesterday = today - timedelta(days=1)
            timesheets = scoped.env['sf.staffing.timesheet'].search([
                ('state', 'in', ('draft', 'confirmed')),
                ('date', '=', yesterday),
            ])
            for timesheet in timesheets:
                timesheet._sf_check_todo(
                    todo_type,
                    'Timesheet %s not validated' % timesheet.name,
                    'Reminder: the timesheet for %s has not been validated.' % timesheet.date,
                )