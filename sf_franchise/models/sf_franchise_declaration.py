# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfFranchiseDeclaration(models.Model):
    _name = 'sf.franchise.declaration'
    _description = 'Franchise Sales Declaration'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.franchise.activity.mixin']
    _order = 'period_start desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    contract_id = fields.Many2one('sf.franchise.contract', string='Franchise Contract',
                                  required=True, ondelete='cascade')
    period_start = fields.Date(string='Period Start', required=True)
    period_end = fields.Date(string='Period End', required=True)
    declared_sales = fields.Monetary(string='Declared Sales', required=True,
                                     currency_field='currency_id')
    royalty_amount = fields.Monetary(string='Royalty Amount', currency_field='currency_id',
                                     compute='_compute_royalty_amount', store=True)
    invoice_id = fields.Many2one('account.move', string='Royalty Invoice', copy=False)
    invoice_state = fields.Selection(related='invoice_id.state', string='Invoice Status',
                                     readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('declared_sales_non_negative', 'CHECK (declared_sales >= 0)',
         'The declared sales cannot be negative.'),
    ]

    @api.depends('declared_sales', 'contract_id.royalty_type', 'contract_id.royalty_percent',
                 'contract_id.fixed_amount')
    def _compute_royalty_amount(self):
        for declaration in self:
            contract = declaration.contract_id
            if contract.royalty_type == 'percentage':
                declaration.royalty_amount = declaration.declared_sales * contract.royalty_percent / 100.0
            else:
                declaration.royalty_amount = contract.fixed_amount or 0.0

    @api.constrains('period_start', 'period_end')
    def _check_period(self):
        for declaration in self:
            if declaration.period_start and declaration.period_end and \
                    declaration.period_start > declaration.period_end:
                raise ValidationError(_('The period start must be before or on the period end.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.franchise.declaration')
            if not vals.get('company_id') and vals.get('contract_id'):
                contract = self.env['sf.franchise.contract'].browse(vals['contract_id'])
                vals['company_id'] = contract.company_id.id
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_franchise.group_sf_franchise_manager'):
            raise UserError(_('Only a franchise manager can perform this action.'))

    def _get_royalty_account(self, company):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_franchise.default_royalty_account_id')
        if param:
            account = self.env['account.account'].browse(int(param))
            if account.exists():
                return account
        return self.env['account.account'].search([
            ('account_type', '=', 'income'),
            ('company_id', '=', company.id),
        ], limit=1)

    def _get_sale_journal(self, company):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_franchise.default_sale_journal_id')
        if param:
            journal = self.env['account.journal'].browse(int(param))
            if journal.exists():
                return journal
        return self.env['account.journal'].search([
            ('company_id', '=', company.id),
            ('type', '=', 'sale'),
        ], limit=1)

    def action_confirm(self):
        self._check_manager()
        for declaration in self:
            if declaration.state != 'draft':
                raise UserError(_('Only draft declarations can be confirmed.'))
            declaration.state = 'confirmed'
            declaration.message_post(body=_('The sales declaration was confirmed.'))

    def action_generate_invoice(self):
        self._check_manager()
        for declaration in self:
            if declaration.state != 'confirmed':
                raise UserError(_('Only confirmed declarations can be invoiced.'))
            company = declaration.company_id
            journal = declaration._get_sale_journal(company)
            account = declaration._get_royalty_account(company)
            if not journal:
                raise UserError(_('No sale journal found for the declaration company.'))
            if not account:
                raise UserError(_('No royalty income account found for the declaration company.'))
            invoice = self.env['account.move'].with_company(company).create({
                'move_type': 'out_invoice',
                'partner_id': declaration.contract_id.partner_id.id,
                'invoice_date': fields.Date.context_today(declaration),
                'journal_id': journal.id,
                'company_id': company.id,
                'invoice_line_ids': [(0, 0, {
                    'name': _('Franchise royalty %s (%s to %s)') % (
                        declaration.contract_id.name, declaration.period_start,
                        declaration.period_end),
                    'quantity': 1,
                    'price_unit': declaration.royalty_amount,
                    'account_id': account.id,
                })],
            })
            invoice.action_post()
            declaration.write({
                'invoice_id': invoice.id,
                'state': 'invoiced',
            })
            declaration.message_post(
                body=_('Royalty invoice %s was generated and posted.') % invoice.name)

    def action_mark_paid(self):
        self._check_manager()
        for declaration in self:
            if declaration.state != 'invoiced':
                raise UserError(_('Only invoiced declarations can be marked as paid.'))
            if not declaration.invoice_id or declaration.invoice_id.state != 'posted':
                raise UserError(_('The related royalty invoice must be posted first.'))
            declaration.state = 'paid'
            declaration.message_post(body=_('The royalty invoice was marked as paid.'))

    def action_cancel(self):
        self._check_manager()
        for declaration in self:
            if declaration.state in ('invoiced', 'paid'):
                raise UserError(_('Invoiced or paid declarations cannot be cancelled.'))
            declaration.state = 'cancelled'
            declaration.message_post(body=_('The declaration was cancelled.'))

    def _cron_daily_checks(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            pending = scoped.env['sf.franchise.declaration'].search([
                ('state', '=', 'confirmed'),
                ('invoice_id', '=', False),
            ])
            for declaration in pending:
                declaration._sf_check_todo(
                    todo_type,
                    _('Royalty declaration %s awaits invoicing') % declaration.name,
                    _('Generate the royalty invoice for this confirmed declaration.'),
                )
            invoiced = scoped.env['sf.franchise.declaration'].search([
                ('state', '=', 'invoiced'),
                ('invoice_id.state', '!=', 'cancel'),
            ]).filtered(lambda d: not d.invoice_id or d.invoice_id.payment_state != 'paid')
            for declaration in invoiced:
                declaration._sf_check_todo(
                    todo_type,
                    _('Royalty invoice of declaration %s is unpaid') % declaration.name,
                    _('Follow up the payment of the royalty invoice.'),
                )

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.franchise.activity.mixin'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.franchise.activity.mixin'

    def action_refresh_business(self):
        """Pull open / overdue amounts for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            moves = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('partner_id', '=', partner.id)])
            open_amt = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
            ).mapped('amount_residual'))
            today = fields.Date.context_today(rec)
            overdue = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
                and m.invoice_date_due
                and m.invoice_date_due < today
            ).mapped('amount_residual'))
            rec.message_post(body=_(
                'Open: {o:.2f}, Overdue: {d:.2f} '
                '({c} posted invoice(s)).').format(
                o=open_amt, d=overdue, c=len(moves)))
        return True
