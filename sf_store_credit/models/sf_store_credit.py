# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfStoreCredit(models.Model):
    _name = 'sf.store.credit'
    _description = 'Store Credit'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.store.credit.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    account_id = fields.Many2one('sf.store.credit.account', string='Credit Account',
                                 required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 related='account_id.partner_id', store=True, readonly=True)
    credit_type = fields.Selection([
        ('granted', 'Granted'),
        ('adjustment', 'Adjustment'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Credit Type', default='granted', required=True)
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    reason = fields.Char(string='Reason')
    expiration_date = fields.Date(string='Expiration Date')
    used_amount = fields.Monetary(string='Used Amount', currency_field='currency_id',
                                  compute='_compute_used_amount', store=True)
    remaining = fields.Monetary(string='Remaining', currency_field='currency_id',
                                compute='_compute_remaining', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('adjusted', 'Adjusted'),
    ], string='Status', default='draft', copy=False)
    sale_order_id = fields.Many2one('sale.order', string='Linked Sales Order', ondelete='set null')
    move_ids = fields.One2many('sf.store.credit.move', 'credit_id', string='Movements')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('amount_positive', 'CHECK (amount > 0)', 'The credit amount must be positive.'),
        ('used_amount_limit', 'CHECK (used_amount >= 0 AND used_amount <= amount)',
         'The used amount cannot exceed the credit amount.'),
        ('remaining_non_negative', 'CHECK (remaining >= 0)',
         'The remaining balance cannot be negative.'),
    ]

    @api.depends('move_ids.move_type', 'move_ids.amount', 'state')
    def _compute_used_amount(self):
        for credit in self:
            used = sum(credit.move_ids.filtered(
                lambda move: move.move_type in ('use', 'adjust')).mapped('amount'))
            credit.used_amount = used

    @api.depends('amount', 'used_amount')
    def _compute_remaining(self):
        for credit in self:
            credit.remaining = credit.amount - credit.used_amount

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.store.credit')
            if not vals.get('company_id') and vals.get('account_id'):
                account = self.env['sf.store.credit.account'].browse(vals['account_id'])
                vals['company_id'] = account.company_id.id
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_store_credit.group_sf_store_credit_manager'):
            raise UserError(_('Only a store credit manager can perform this action.'))

    def action_confirm(self):
        self._check_manager()
        for credit in self:
            if credit.state != 'draft':
                raise UserError(_('Only draft credits can be confirmed.'))
            credit.state = 'confirmed'
            credit.credit_type = 'granted'
            self.env['sf.store.credit.move'].create({
                'credit_id': credit.id,
                'move_type': 'grant',
                'amount': credit.amount,
                'reason': credit.reason or _('Credit granted'),
                'company_id': credit.company_id.id,
            })
            credit.message_post(body=_('The credit was confirmed and is now available.'))

    def action_use(self, amount, sale_order_id=False):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed credits can be used.'))
        if self.expiration_date and self.expiration_date < \
                fields.Date.context_today(self):
            raise UserError(_('This credit has expired and can no longer be used.'))
        if amount <= 0:
            raise UserError(_('The amount to use must be positive.'))
        if amount > self.remaining:
            raise UserError(_('The amount exceeds the remaining balance of the credit.'))
        self.env['sf.store.credit.move'].create({
            'credit_id': self.id,
            'move_type': 'use',
            'amount': amount,
            'reason': _('Credit used on a sale'),
            'sale_order_id': sale_order_id,
            'company_id': self.company_id.id,
        })
        if sale_order_id:
            self.sale_order_id = sale_order_id
        if self.remaining <= 0:
            self.state = 'used'
            self.credit_type = 'used'
        self.message_post(body=_('Credit used: %s') % amount)

    def action_use_remaining(self):
        for credit in self:
            credit.action_use(credit.remaining)

    def action_adjust(self, amount, reason):
        self._check_manager()
        for credit in self:
            if credit.state != 'confirmed':
                raise UserError(_('Only confirmed credits can be adjusted.'))
            if amount <= 0:
                raise UserError(_('The adjustment amount must be positive.'))
            if amount > credit.remaining:
                raise UserError(_('The adjustment exceeds the remaining balance of the credit.'))
            self.env['sf.store.credit.move'].create({
                'credit_id': credit.id,
                'move_type': 'adjust',
                'amount': amount,
                'reason': reason or _('Manual adjustment'),
                'company_id': credit.company_id.id,
            })
            if credit.remaining <= 0:
                credit.state = 'adjusted'
                credit.credit_type = 'adjustment'
            credit.message_post(body=_('Credit adjusted by %s.') % amount)

    def action_cancel(self):
        self._check_manager()
        for credit in self:
            if credit.state not in ('draft', 'confirmed'):
                raise UserError(_('Only draft or confirmed credits can be cancelled.'))
            if credit.used_amount > 0:
                raise UserError(_('A credit that has already been used cannot be cancelled.'))
            credit.state = 'cancelled'
            credit.credit_type = 'cancelled'
            self.env['sf.store.credit.move'].create({
                'credit_id': credit.id,
                'move_type': 'cancel',
                'amount': credit.amount,
                'reason': _('Credit cancelled'),
                'company_id': credit.company_id.id,
            })
            credit.message_post(body=_('The credit was cancelled.'))

    def action_open_adjust_wizard(self):
        self.ensure_one()
        return {
            'name': _('Adjust Credit'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.store.credit.adjust.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_credit_id': self.id},
        }

    def _cron_daily_checks(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        reminder_param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_store_credit.expiry_reminder_days', '7')
        reminder_days = int(reminder_param)
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            expired = scoped.env['sf.store.credit'].search([
                ('state', '=', 'confirmed'),
                ('expiration_date', '!=', False),
                ('expiration_date', '<', today),
            ])
            for credit in expired:
                credit.state = 'expired'
                credit.credit_type = 'expired'
                self.env['sf.store.credit.move'].create({
                    'credit_id': credit.id,
                    'move_type': 'expire',
                    'amount': credit.remaining,
                    'reason': _('Credit expired'),
                    'company_id': credit.company_id.id,
                })
                credit.message_post(body=_('The credit expired.'))
            threshold = today + timedelta(days=reminder_days)
            upcoming = scoped.env['sf.store.credit'].search([
                ('state', '=', 'confirmed'),
                ('expiration_date', '!=', False),
                ('expiration_date', '>=', today),
                ('expiration_date', '<=', threshold),
            ])
            for credit in upcoming:
                credit._sf_check_todo(
                    todo_type,
                    _('Credit %s is about to expire') % credit.name,
                    _('The credit expires on %s.') % credit.expiration_date,
                )


class SfStoreCreditMove(models.Model):
    _name = 'sf.store.credit.move'
    _description = 'Store Credit Movement'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.store.credit.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    credit_id = fields.Many2one('sf.store.credit', string='Credit', required=True,
                                ondelete='cascade')
    move_type = fields.Selection([
        ('grant', 'Grant'),
        ('use', 'Use'),
        ('adjust', 'Adjustment'),
        ('expire', 'Expiration'),
        ('cancel', 'Cancellation'),
    ], string='Type', required=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    reason = fields.Char(string='Reason')
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', ondelete='set null')
    date = fields.Date(string='Date', default=lambda self: fields.Date.context_today(self))
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.store.credit.move')
            if not vals.get('company_id') and vals.get('credit_id'):
                credit = self.env['sf.store.credit'].browse(vals['credit_id'])
                vals['company_id'] = credit.company_id.id
        return super().create(vals_list)