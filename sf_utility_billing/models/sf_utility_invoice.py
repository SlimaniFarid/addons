# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfUtilityInvoice(models.Model):
    _name = 'sf.utility.invoice'
    _description = 'Utility Consumption Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.utility.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    meter_id = fields.Many2one('sf.utility.meter', string='Meter', required=True, ondelete='restrict')
    campaign_id = fields.Many2one('sf.utility.campaign', string='Campaign', ondelete='set null')
    reading_id = fields.Many2one('sf.utility.meter.reading', string='Reading', ondelete='set null')
    consumption = fields.Float(string='Consumption')
    amount_total = fields.Monetary(string='Amount', compute='_compute_amount', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    invoice_id = fields.Many2one('account.move', string='Accounting Invoice', readonly=True, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('consumption', 'meter_id', 'campaign_id')
    def _compute_amount(self):
        for invoice in self:
            invoice.amount_total = self._apply_tariff(invoice.meter_id, invoice.campaign_id, invoice.consumption)

    def _apply_tariff(self, meter, campaign, consumption):
        if not meter or not campaign or not consumption:
            return 0.0
        company = meter.company_id or self.env.company
        tariff = self.env['sf.utility.tariff'].search([
            ('utility_type', '=', meter.utility_type),
            ('effective_from', '<=', campaign.period_end),
            ('active', '=', True),
            ('company_id', '=', company.id),
        ], order='effective_from desc, id desc', limit=1)
        if not tariff:
            return 0.0
        total = 0.0
        for line in tariff.line_ids.sorted(key=lambda l: l.from_quantity):
            upper = line.to_quantity if line.to_quantity else float('inf')
            overlap = min(consumption, upper) - min(consumption, line.from_quantity)
            if overlap > 0:
                total += overlap * line.price_per_unit
        return total

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.utility.invoice')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_utility_billing.group_sf_utility_manager'):
            raise UserError(_('Only a utility manager can perform this action.'))

    def _get_revenue_account(self):
        self.ensure_one()
        account = self.env['account.account']
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_utility_billing.default_revenue_account')
        if param:
            try:
                account = account.browse(int(param))
                if not account.exists() or account.company_id.id != self.company_id.id:
                    account = account.browse()
            except (TypeError, ValueError):
                account = account.browse()
        if not account:
            account = self.env['account.account'].search([
                ('account_type', '=', 'income'),
                ('company_id', '=', self.company_id.id),
            ], limit=1)
        return account

    def _prepare_account_move(self):
        self.ensure_one()
        journal = self.env['account.journal'].search([
            ('company_id', '=', self.company_id.id),
            ('type', '=', 'sale'),
        ], limit=1)
        account = self._get_revenue_account()
        return {
            'move_type': 'out_invoice',
            'partner_id': self.meter_id.partner_id.id,
            'invoice_date': fields.Date.context_today(self),
            'journal_id': journal.id if journal else False,
            'invoice_line_ids': [(0, 0, {
                'name': 'Consumption invoice %s' % self.name,
                'quantity': 1,
                'price_unit': self.amount_total,
                'account_id': account.id if account else False,
            })],
        }

    def action_post(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft invoices can be posted.'))
        move = self.env['account.move'].create(self._prepare_account_move())
        if not (move.line_ids and all(line.account_id for line in move.line_ids)):
            move.unlink()
            raise UserError(_(
                'The accounting move could not be posted: no valid income account. '
                'Configure the default revenue account.'))
        move.action_post()
        self.invoice_id = move.id
        self.state = 'posted'

    def action_paid(self):
        self.ensure_one()
        if self.state not in ('posted', 'overdue'):
            raise UserError(_('Only posted invoices can be marked paid.'))
        self.state = 'paid'

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('paid', 'overdue'):
            raise UserError(_('Paid or overdue invoices cannot be cancelled.'))
        if self.invoice_id:
            if self.invoice_id.state == 'posted':
                raise UserError(_(
                    'The accounting invoice is posted; it must be reversed before '
                    'this consumption invoice can be cancelled.'))
            self.invoice_id.unlink()
        self.invoice_id = False
        self.state = 'cancelled'

    def _cron_daily_checks(self):
        overdue = self.search([
            ('state', '=', 'posted'),
            ('invoice_id', '!=', False),
        ]).filtered(
            lambda inv: inv.invoice_id.payment_state != 'paid'
            and inv.invoice_id.invoice_date_due
            and inv.invoice_id.invoice_date_due < fields.Date.context_today(inv)
        )
        for invoice in overdue:
            invoice.state = 'overdue'