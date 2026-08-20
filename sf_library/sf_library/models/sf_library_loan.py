# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLibraryLoan(models.Model):
    _name = 'sf.library.loan'
    _description = 'Library Loan'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    item_id = fields.Many2one(
        'sf.library.item', string='Item', ondelete='restrict',
        index=True, required=True, tracking=True)
    member_id = fields.Many2one(
        'sf.library.member', string='Member', ondelete='restrict',
        index=True, required=True, tracking=True)
    loan_date = fields.Date(
        string='Loan date', default=fields.Date.context_today, tracking=True)
    due_date = fields.Date(string='Due date', tracking=True)
    return_date = fields.Date(string='Return date', tracking=True)
    late_days = fields.Integer(
        string='Late days', compute='_compute_late_days', store=True)
    late_fee = fields.Float(
        string='Late fee', compute='_compute_late_fee', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('on_loan', 'On loan'),
        ('returned', 'Returned'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('due_date', 'return_date', 'state')
    def _compute_late_days(self):
        for loan in self:
            if not loan.due_date:
                loan.late_days = 0
                continue
            end = loan.return_date or fields.Date.today()
            days = (end - loan.due_date).days
            loan.late_days = days if days > 0 else 0

    @api.depends('late_days', 'company_id.sf_library_fine_per_day')
    def _compute_late_fee(self):
        for loan in self:
            loan.late_fee = loan.late_days * loan.company_id.sf_library_fine_per_day

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.library.loan')
        return super().create(vals)

    def action_confirm(self):
        for loan in self:
            if loan.state != 'draft':
                raise UserError(_('Only draft loans can be confirmed.'))
            if loan.member_id.status == 'blocked':
                raise UserError(_('A blocked member cannot take out a new loan.'))
            if loan.item_id.available_copies < 1:
                raise UserError(_('No copy of this item is available.'))
            loan.due_date = loan.loan_date + timedelta(
                days=loan.company_id.sf_library_loan_days)
        self.state = 'on_loan'

    def action_return(self):
        if not self.env.user.has_group('sf_library.group_sf_library_manager'):
            raise UserError(_('Only a library manager can validate a return.'))
        for loan in self:
            if loan.state != 'on_loan':
                raise UserError(_('Only on-loan records can be returned.'))
            loan.return_date = fields.Date.today()
        self.state = 'returned'
        self.env['sf.library.reservation']._process_ready_reservations()

    def _cron_library_alerts(self):
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            late_loans = self.with_company(company).search([
                ('state', '=', 'on_loan'),
                ('due_date', '<', today),
                ('return_date', '=', False),
            ])
            for loan in late_loans:
                if loan.activity_ids.filtered(
                        lambda a: a.activity_type_id == self.env.ref(
                            'mail.mail_activity_data_todo')):
                    continue
                loan.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Late loan: %s') % loan.name,
                    user_id=self.env.user.id)
            ready_reservations = self.env['sf.library.reservation'].with_company(
                company).search([
                    ('status', '=', 'ready'),
                    ('expiry_date', '<=', today + timedelta(days=3)),
                ])
            for reservation in ready_reservations:
                if reservation.activity_ids.filtered(
                        lambda a: a.activity_type_id == self.env.ref(
                            'mail.mail_activity_data_todo')):
                    continue
                reservation.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Ready reservation expiring: %s') % reservation.name,
                    user_id=self.env.user.id)
