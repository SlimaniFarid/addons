# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCleaningContract(models.Model):
    _name = 'sf.cleaning.contract'
    _description = 'Cleaning Service Contract'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Client', ondelete='restrict',
        required=True, tracking=True)
    contract_type = fields.Selection([
        ('recurring', 'Recurring'),
        ('one_time', 'One-time'),
    ], string='Contract type', default='recurring', required=True,
       tracking=True)
    date_start = fields.Date(string='Start date', tracking=True)
    date_end = fields.Date(string='End date', tracking=True)
    billing_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('bimonthly', 'Bimonthly'),
        ('quarterly', 'Quarterly'),
    ], string='Billing period', default='monthly', required=True,
       tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    line_ids = fields.One2many(
        'sf.cleaning.contract.line', 'contract_id', string='Site lines')
    schedule_ids = fields.One2many(
        'sf.cleaning.schedule', 'contract_id', string='Schedules')
    overdue_quality_check_count = fields.Integer(
        string='Overdue quality checks', compute='_compute_overdue_quality_check_count',
        store=True)
    note = fields.Text(string='Notes')

    @api.depends('schedule_ids.line_ids.quality_check_id.state',
                 'schedule_ids.line_ids.quality_check_id.check_date')
    def _compute_overdue_quality_check_count(self):
        for contract in self:
            today = fields.Date.context_today(contract)
            overdue = 0
            for line in contract.schedule_ids.line_ids:
                qc = line.quality_check_id
                if qc and qc.state == 'draft' and qc.check_date \
                        and qc.check_date < today:
                    overdue += 1
            contract.overdue_quality_check_count = overdue

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.cleaning.contract')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_cleaning.group_sf_cleaning_manager'):
            raise UserError(_('Only managers can perform this action.'))

    def unlink(self):
        self._check_manager()
        return super().unlink()

    def action_activate(self):
        self._check_manager()
        for contract in self:
            if contract.state != 'draft':
                raise UserError(_('Only draft contracts can be activated.'))
            if not contract.line_ids:
                raise UserError(_('A contract cannot be activated without at '
                                  'least one site line.'))
        self.state = 'active'

    def action_suspend(self):
        self._check_manager()
        for contract in self:
            if contract.state != 'active':
                raise UserError(_('Only active contracts can be suspended.'))
        self.state = 'suspended'

    def action_resume(self):
        self._check_manager()
        for contract in self:
            if contract.state != 'suspended':
                raise UserError(_('Only suspended contracts can be resumed.'))
        self.state = 'active'

    def action_done(self):
        self._check_manager()
        for contract in self:
            if contract.state not in ('active', 'suspended'):
                raise UserError(_('Only active or suspended contracts can be '
                                  'closed.'))
        self.state = 'done'

    def action_cancel(self):
        self._check_manager()
        for contract in self:
            if contract.state not in ('draft', 'active', 'suspended'):
                raise UserError(_('Only draft, active or suspended contracts '
                                  'can be cancelled.'))
        self.state = 'cancelled'