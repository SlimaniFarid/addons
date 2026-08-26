# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfParkingSubscription(models.Model):
    _name = 'sf.parking.subscription'
    _description = 'Parking Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.parking.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='restrict')
    site_id = fields.Many2one('sf.parking.site', string='Site', required=True, ondelete='restrict')
    place_id = fields.Many2one('sf.parking.place', string='Place', ondelete='set null',
                               domain="[('site_id', '=', site_id), ('state', '=', 'free')]")
    vehicle_plate = fields.Char(string='Vehicle Plate')
    billing_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Billing Period', required=True, default='monthly')
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('renewed', 'Renewed'),
    ], string='Status', default='draft', copy=False)
    invoice_ids = fields.Many2many('account.move', string='Invoices', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model
    def _period_delta(self, billing_period):
        if billing_period == 'yearly':
            return relativedelta(years=1)
        if billing_period == 'quarterly':
            return relativedelta(months=3)
        return relativedelta(months=1)

    @api.model
    def _next_end_date(self, start_date, billing_period):
        return start_date + self._period_delta(billing_period)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.parking.subscription')
            if not vals.get('end_date') and vals.get('start_date'):
                vals['end_date'] = self._next_end_date(
                    vals['start_date'], vals.get('billing_period', 'monthly'))
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_parking_management.group_sf_parking_manager'):
            raise UserError(_('Only a parking manager can perform this action.'))

    def _get_revenue_account(self):
        account_id = self.env['ir.config_parameter'].sudo().get_param(
            'sf_parking_management.revenue_account_id')
        if account_id:
            account = self.env['account.account'].browse(int(account_id))
            if account.exists():
                return account.id
        account = self.env['account.account'].search([
            ('account_type', '=', 'income'),
            ('company_id', '=', self.company_id.id),
        ], limit=1)
        return account.id if account else False

    def _generate_invoice(self):
        self.ensure_one()
        journal = self.env['account.journal'].search([
            ('company_id', '=', self.company_id.id),
            ('type', '=', 'sale'),
        ], limit=1)
        if not journal:
            raise UserError(_('No sale journal found for the subscription company.'))
        invoice = self.env['account.move'].with_company(self.company_id).create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'journal_id': journal.id,
            'invoice_line_ids': [(0, 0, {
                'name': _('Parking subscription %s (%s)') % (self.name, self.billing_period),
                'quantity': 1,
                'price_unit': self.amount,
                'account_id': self._get_revenue_account() or False,
            })],
        })
        if invoice.line_ids and all(line.account_id for line in invoice.line_ids):
            invoice.action_post()
        self.invoice_ids = [(4, invoice.id)]
        return invoice

    def action_activate(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft subscriptions can be activated.'))
        if self.place_id and self.place_id.state in ('occupied', 'reserved', 'out_of_service'):
            raise UserError(_('The place is not available.'))
        if not self.end_date:
            self.end_date = self._next_end_date(self.start_date, self.billing_period)
        self._generate_invoice()
        self.state = 'active'
        if self.place_id:
            self.place_id.state = 'reserved'

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state == 'active' and self.place_id and self.place_id.state == 'reserved':
            self.place_id.state = 'free'
        self.state = 'cancelled'

    def _renew(self):
        self.ensure_one()
        if not self.end_date:
            raise UserError(_('The subscription has no end date to renew.'))
        self._generate_invoice()
        self.end_date = self.end_date + self._period_delta(self.billing_period)
        self.state = 'renewed'
        self.message_post(body=_('Subscription renewed and invoiced until %s.') % self.end_date)

    def _expire(self, todo_type=None):
        self.ensure_one()
        self.state = 'expired'
        if self.place_id and self.place_id.state == 'reserved':
            self.place_id.state = 'free'
        if todo_type:
            self._sf_check_todo(
                todo_type,
                'Subscription %s has expired' % self.name,
                'Reminder: renew the subscription or release the place.',
            )

    def _cron_daily_checks(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            due = scoped.env['sf.parking.subscription'].search([
                ('state', 'in', ('active', 'renewed')),
                ('end_date', '<=', today),
            ])
            for subscription in due:
                try:
                    subscription._renew()
                except UserError:
                    subscription._expire(todo_type)