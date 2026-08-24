# -*- coding: utf-8 -*-
"""Lease contract models - IFRS 16 / ASC 842 lessee accounting."""
import calendar
import dateutil.relativedelta as rd

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SfLeaseContract(models.Model):
    """Lease contract with ROU asset and lease liability measurement."""
    _name = 'sf.lease.contract'
    _description = 'Lease Contract (IFRS 16 / ASC 842)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Lease Reference', required=True, copy=False,
                       readonly=True, default='New')
    display_description = fields.Char(string='Description', required=True)
    lessor_id = fields.Many2one('res.partner', string='Lessor (Landlord/Vendor)',
                                required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company, tracking=True)
    currency_id = fields.Many2one(related='company_id.currency_id')
    asset_category = fields.Selection([
        ('real_estate', 'Real Estate'),
        ('vehicle', 'Vehicle / Fleet'),
        ('equipment', 'Equipment / Machinery'),
        ('it', 'IT / Software Hosting'),
        ('other', 'Other'),
    ], string='Asset Category', required=True, default='real_estate', tracking=True)

    # Terms
    start_date = fields.Date(string='Commencement Date', required=True,
                             default=fields.Date.today, tracking=True)
    term_months = fields.Integer(string='Lease Term (months)', required=True, default=36)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    payment_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ], string='Payment Frequency', required=True, default='monthly')
    payment_amount = fields.Monetary(string='Payment per Period', required=True)
    payment_timing = fields.Selection([
        ('arrears', 'In Arrears (end of period)'),
        ('advance', 'In Advance (start of period)'),
    ], required=True, default='arrears')
    incremental_borrowing_rate = fields.Float(
        string='IBR % (annual)', required=True, default=5.0,
        help='Incremental Borrowing Rate used to discount lease payments.')

    # Initial measurement components
    initial_direct_costs = fields.Monetary(string='Initial Direct Costs', default=0.0)
    incentives_received = fields.Monetary(string='Lease Incentives Received', default=0.0)
    prepaid_rent = fields.Monetary(string='Prepaid Rent at Commencement', default=0.0)
    restoration_costs = fields.Monetary(string='Restoration / Dismantling Costs', default=0.0)

    # Exemptions
    short_term_exemption = fields.Boolean(
        string='Short-term Exemption (<= 12 months)',
        help='IFRS 16 para 6 / ASC 842-20-25-2: expense payments straight-line.')
    low_value_exemption = fields.Boolean(
        string='Low-value Exemption (<= USD 5,000)',
        help='IFRS 16 para 5(b): expense payments straight-line.')
    is_exempt = fields.Boolean(compute='_compute_is_exempt')

    # Computed measurements
    lease_liability_initial = fields.Monetary(
        string='Initial Lease Liability (PV)', compute='_compute_measurements',
        store=True, help='Present value of remaining payments discounted at IBR.')
    rou_asset_initial = fields.Monetary(
        string='Initial ROU Asset', compute='_compute_measurements', store=True,
        help='Liability + direct costs + prepaid + restoration - incentives.')
    monthly_depreciation = fields.Monetary(
        string='Depreciation per Period', compute='_compute_measurements', store=True)

    # Accounts & journals
    rou_asset_account_id = fields.Many2one(
        'account.account', string='ROU Asset Account',
        domain=[('account_type', '=', 'asset_fixed')])
    accumulated_depreciation_account_id = fields.Many2one(
        'account.account', string='Accumulated Depreciation Account',
        domain=[('account_type', '=', 'asset_fixed')])
    interest_expense_account_id = fields.Many2one(
        'account.account', string='Interest Expense Account',
        domain=[('account_type', '=', 'expense')])
    depreciation_expense_account_id = fields.Many2one(
        'account.account', string='Depreciation Expense Account',
        domain=[('account_type', '=', 'expense')])
    lease_expense_account_id = fields.Many2one(
        'account.account', string='Straight-line Lease Expense Account (exempt)',
        domain=[('account_type', '=', 'expense')])
    payment_journal_id = fields.Many2one('account.journal', string='Payment Journal',
                                         domain=[('type', 'in', ('bank', 'cash'))])

    # Schedule
    payment_line_ids = fields.One2many('sf.lease.payment.line', 'contract_id',
                                       string='Payment Schedule')

    # ASC 842 informational classification
    asc842_classification = fields.Selection([
        ('finance', 'Finance Lease'),
        ('operating', 'Operating Lease'),
    ], string='ASC 842 Classification', default='operating',
        help='Informational for US GAAP dual-model reporting. '
             'IFRS 16 uses a single lessee model.')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('modified', 'Modified'),
        ('terminated', 'Terminated Early'),
        ('closed', 'Closed - Fully Amortized'),
    ], string='Status', default='draft', tracking=True, copy=False)
    modification_ids = fields.One2many('sf.lease.modification', 'contract_id',
                                       string='Modifications / Reassessments')
    modification_count = fields.Integer(compute='_compute_modification_count')
    fully_posted = fields.Boolean(compute='_compute_fully_posted')

    _sql_constraints = [
        ('positive_term', 'CHECK(term_months > 0)',
         'Lease term must be strictly positive.'),
        ('positive_payment', 'CHECK(payment_amount >= 0)',
         'Payment amount cannot be negative.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.lease.contract') or 'LEASE-NEW'
        return super().create(vals_list)

    @api.depends('start_date', 'term_months')
    def _compute_end_date(self):
        for contract in self:
            if contract.start_date and contract.term_months:
                contract.end_date = contract.start_date + rd.relativedelta(
                    months=contract.term_months, days=-1)
            else:
                contract.end_date = False

    @api.depends('short_term_exemption', 'low_value_exemption')
    def _compute_is_exempt(self):
        for contract in self:
            contract.is_exempt = bool(
                contract.short_term_exemption or contract.low_value_exemption)

    @api.depends('payment_line_ids')
    def _compute_fully_posted(self):
        for contract in self:
            lines = contract.payment_line_ids
            contract.fully_posted = bool(lines) and all(l.posted for l in lines)

    def _compute_modification_count(self):
        for contract in self:
            contract.modification_count = len(contract.modification_ids)

    @api.depends('payment_amount', 'payment_frequency', 'payment_timing',
                 'incremental_borrowing_rate', 'term_months', 'start_date',
                 'initial_direct_costs', 'incentives_received', 'prepaid_rent',
                 'restoration_costs', 'is_exempt', 'state')
    def _compute_measurements(self):
        for contract in self:
            if contract.is_exempt:
                contract.lease_liability_initial = 0.0
                contract.rou_asset_initial = 0.0
                contract.monthly_depreciation = 0.0
                continue
            periods_per_year = contract._periods_per_year()
            rate = contract.incremental_borrowing_rate / 100.0 / periods_per_year
            n = contract._number_of_periods()
            payment = contract.payment_amount
            pv = 0.0
            for t in range(n):
                exponent = t if contract.payment_timing == 'advance' else t + 1
                pv += payment / ((1.0 + rate) ** exponent)
            contract.lease_liability_initial = round(pv, 2)
            rou = (pv + contract.initial_direct_costs + contract.prepaid_rent
                   + contract.restoration_costs - contract.incentives_received)
            contract.rou_asset_initial = max(rou, 0.0)
            contract.monthly_depreciation = round(
                contract.rou_asset_initial / max(n, 1), 2)

    # -------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------
    def _periods_per_year(self):
        self.ensure_one()
        return {'monthly': 12, 'quarterly': 4, 'annual': 1}[self.payment_frequency]

    def _number_of_periods(self):
        self.ensure_one()
        ppy = self._periods_per_year()
        return max(1, int(round(self.term_months * ppy / 12.0)))

    def _period_delta(self):
        self.ensure_one()
        return {'monthly': rd.relativedelta(months=1),
                'quarterly': rd.relativedelta(months=3),
                'annual': rd.relativedelta(years=1)}[self.payment_frequency]

    def _add_period(self, date, index):
        """Start date + (index or index+1) periods, clamped to month end."""
        self.ensure_one()
        delta = self._period_delta()
        offset = index if self.payment_timing == 'advance' else index + 1
        target = date + (delta * offset)
        last_day = calendar.monthrange(target.year, target.month)[1]
        return target.replace(day=min(target.day, last_day))

    # -------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------
    def action_generate_schedule(self):
        """(Re)build the full payment schedule with amortization."""
        for contract in self:
            contract.payment_line_ids.unlink()
            if contract.state not in ('draft', 'active', 'modified'):
                raise UserError(_('Schedule can only be generated on Draft, '
                                  'Active or Modified contracts.'))
            n = contract._number_of_periods()
            ppy = contract._periods_per_year()
            rate = contract.incremental_borrowing_rate / 100.0 / ppy
            opening = contract.rou_asset_initial if not contract.is_exempt else 0.0
            liability = contract.lease_liability_initial
            vals_list = []
            for t in range(n):
                due_date = contract._add_period(contract.start_date, t)
                if contract.is_exempt:
                    interest = 0.0
                    principal = contract.payment_amount
                    liability = 0.0
                else:
                    if contract.payment_timing == 'advance':
                        principal = contract.payment_amount - liability * rate
                        interest = liability * rate - contract.payment_amount + principal
                        # interest accrued on balance after advance payment
                        interest = max(0.0, liability * rate)
                        principal = contract.payment_amount - interest
                    else:
                        interest = liability * rate
                        principal = contract.payment_amount - interest
                    closing = liability - principal
                vals_list.append({
                    'contract_id': contract.id,
                    'sequence': t + 1,
                    'period_index': t + 1,
                    'due_date': due_date,
                    'payment_amount': contract.payment_amount,
                    'opening_liability': round(liability, 2),
                    'interest': round(interest, 2),
                    'principal': round(principal, 2),
                    'closing_liability': round(liability - principal, 2),
                    'depreciation': contract.monthly_depreciation,
                })
                liability -= principal
            self.env['sf.lease.payment.line'].create(vals_list)

    def action_activate(self):
        for contract in self:
            if not contract.payment_line_ids:
                contract.action_generate_schedule()
            contract.write({'state': 'active'})

    def action_reopen_draft(self):
        self.write({'state': 'draft'})

    def action_terminate(self):
        self.write({'state': 'terminated'})

    def action_close(self):
        for contract in self:
            if not contract.fully_posted:
                raise UserError(
                    _('All periods must be posted before closing the lease.'))
            contract.write({'state': 'closed'})

    def action_post_due_entries(self):
        """Post journal entries for all due, unposted periods."""
        moves = self.env['account.move']
        today = fields.Date.context_today(self)
        for contract in self:
            if contract.state not in ('active', 'modified'):
                continue
            contract._check_accounts()
            for line in contract.payment_line_ids.filtered(
                    lambda l: not l.posted and l.due_date <= today):
                moves |= contract._create_move_for_line(line)
        if moves:
            moves.action_post()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Posted Journal Entries'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', moves.ids)],
        } if moves else {'type': 'ir.actions.act_window_close'}

    def _check_accounts(self):
        self.ensure_one()
        required = ['payment_journal_id', 'interest_expense_account_id',
                    'rou_asset_account_id', 'accumulated_depreciation_account_id',
                    'depreciation_expense_account_id']
        if self.is_exempt:
            required = ['payment_journal_id', 'lease_expense_account_id']
        missing = [f for f in required if not self[f]]
        if missing:
            raise UserError(_(
                'Missing accounting configuration on lease %s: %s'
            ) % (self.name, ', '.join(missing)))

    def _create_move_for_line(self, line):
        self.ensure_one()
        move_vals = {
            'move_type': 'entry',
            'date': line.due_date,
            'ref': '%s - Period %s' % (self.name, line.period_index),
            'journal_id': self.payment_journal_id.id,
            'company_id': self.company_id.id,
            'line_ids': [],
        }
        lines = []
        payment = line.payment_amount
        if self.is_exempt:
            lines.append((0, 0, {
                'name': _('Lease expense %s P%s') % (self.name, line.period_index),
                'account_id': self.lease_expense_account_id.id,
                'debit': payment, 'credit': 0.0,
            }))
        else:
            lines.append((0, 0, {
                'name': _('Interest %s P%s') % (self.name, line.period_index),
                'account_id': self.interest_expense_account_id.id,
                'debit': line.interest, 'credit': 0.0,
            }))
            lines.append((0, 0, {
                'name': _('Lease liability repayment %s P%s')
                        % (self.name, line.period_index),
                'account_id': self._liability_account().id,
                'debit': line.principal, 'credit': 0.0,
            }))
            lines.append((0, 0, {
                'name': _('ROU depreciation %s P%s') % (self.name, line.period_index),
                'account_id': self.depreciation_expense_account_id.id,
                'debit': line.depreciation, 'credit': 0.0,
            }))
            lines.append((0, 0, {
                'name': _('Accumulated ROU depreciation %s P%s')
                        % (self.name, line.period_index),
                'account_id': self.accumulated_depreciation_account_id.id,
                'debit': 0.0, 'credit': line.depreciation,
            }))
        lines.append((0, 0, {
            'name': _('Lease payment %s P%s') % (self.name, line.period_index),
            'account_id': self.payment_journal_id.payment_credit_account_id.id
            or self._liability_account().id,
            'debit': 0.0, 'credit': payment,
        }))
        move_vals['line_ids'] = lines
        move = self.env['account.move'].create(move_vals)
        line.write({'posted': True, 'move_id': move.id})
        return move

    def _liability_account(self):
        """Fallback liability account: lease liability mapped on ROU account
        payable side. Uses company default lease liability account when set."""
        self.ensure_one()
        account = self.env['ir.config_parameter'].sudo().get_param(
            'sf_lease_ifrs16.liability_account_id')
        if account:
            return self.env['account.account'].browse(int(account))
        return self.env['account.account'].search(
            [('account_type', '=', 'liability_current')], limit=1)

    def action_view_schedule_report(self):
        self.ensure_one()
        return self.env.ref(
            'sf_lease_ifrs16.action_report_lease_schedule').report_action(self)


class SfLeasePaymentLine(models.Model):
    """One period of the lease amortization schedule."""
    _name = 'sf.lease.payment.line'
    _description = 'Lease Payment Schedule Line'
    _order = 'contract_id, sequence'

    contract_id = fields.Many2one('sf.lease.contract', string='Lease Contract',
                                  required=True, ondelete='cascade')
    sequence = fields.Integer(default=1)
    period_index = fields.Integer(string='Period #')
    due_date = fields.Date(string='Due Date', required=True)
    payment_amount = fields.Monetary(string='Payment')
    opening_liability = fields.Monetary(string='Opening Liability')
    interest = fields.Monetary(string='Interest')
    principal = fields.Monetary(string='Principal Repayment')
    closing_liability = fields.Monetary(string='Closing Liability')
    depreciation = fields.Monetary(string='ROU Depreciation')
    posted = fields.Boolean(string='Posted', default=False, copy=False)
    move_id = fields.Many2one('account.move', string='Journal Entry',
                              readonly=True, copy=False)
    currency_id = fields.Many2one(related='contract_id.currency_id')
    company_id = fields.Many2one(related='contract_id.company_id', store=True)
    state = fields.Selection(related='contract_id.state')
