# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DebtCollectionCase(models.Model):
    _name = 'sf.debt.collection.case'
    _description = 'Collection Case'
    _order = 'priority, date_open asc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False)
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        index=True,
        tracking=True,
    )
    collector_id = fields.Many2one(
        'res.users',
        string='Collector',
        tracking=True,
        default=lambda self: self.env.user,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )
    date_open = fields.Date(
        string='Opened On',
        default=fields.Date.context_today,
        readonly=True,
    )
    priority = fields.Selection(
        [
            ('0', 'Normal'),
            ('1', 'Important'),
            ('2', 'Very Important'),
            ('3', 'Urgent'),
        ],
        string='Priority',
        default='0',
        index=True,
    )
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('in_progress', 'In Progress'),
            ('promise', 'Promise'),
            ('done', 'Resolved'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='open',
        tracking=True,
    )
    total_due = fields.Monetary(
        string='Total Due',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
    )
    total_overdue = fields.Monetary(
        string='Total Overdue',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=True,
    )
    days_overdue = fields.Integer(
        string='Days Overdue',
        compute='_compute_days_overdue',
        store=True,
    )
    invoice_line_ids = fields.One2many(
        'sf.debt.invoice.line',
        'case_id',
        string='Overdue Invoices',
    )
    action_ids = fields.One2many(
        'sf.debt.action',
        'case_id',
        string='Actions',
    )
    promise_ids = fields.One2many(
        'sf.debt.promise',
        'case_id',
        string='Payment Promises',
    )
    next_promise_date = fields.Date(
        string='Next Promise Date',
        compute='_compute_next_promise',
        store=True,
    )
    note = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.debt.collection.case')
        return super().create(vals_list)

    @api.depends('invoice_line_ids.amount_due', 'invoice_line_ids.date_maturity',
                 'invoice_line_ids.overdue')
    def _compute_amounts(self):
        today = fields.Date.context_today(self)
        for case in self:
            total_due = sum(case.invoice_line_ids.mapped('amount_due'))
            overdue = sum(
                line.amount_due for line in case.invoice_line_ids
                if line.overdue)
            case.total_due = total_due
            case.total_overdue = overdue

    @api.depends('invoice_line_ids.date_maturity')
    def _compute_days_overdue(self):
        today = fields.Date.context_today(self)
        for case in self:
            overdue_lines = case.invoice_line_ids.filtered('overdue')
            case.days_overdue = max(
                (today - line.date_maturity).days
                for line in overdue_lines) if overdue_lines else 0

    @api.depends('promise_ids.date', 'promise_ids.state')
    def _compute_next_promise(self):
        today = fields.Date.context_today(self)
        for case in self:
            future = case.promise_ids.filtered(
                lambda p: p.state == 'pending' and p.date >= today)
            case.next_promise_date = future[0].date if future else False

    def action_set_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_mark_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_open(self):
        self.write({'state': 'open'})

    def action_refresh_invoices(self):
        self.ensure_one()
        today = fields.Date.context_today(self)
        lines = self.env['account.move.line'].search([
            ('partner_id', '=', self.partner_id.id),
            ('account_id.account_type', '=', 'asset_receivable'),
            ('move_id.state', '=', 'posted'),
            ('amount_residual', '>', 0),
            ('date_maturity', '!=', False),
        ])
        existing = self.invoice_line_ids.mapped('move_line_id').ids
        for line in lines:
            if line.id in existing:
                continue
            self.env['sf.debt.invoice.line'].create({
                'case_id': self.id,
                'move_line_id': line.id,
                'invoice_id': line.move_id.id,
                'invoice_number': line.move_id.name,
                'date_invoice': line.move_id.invoice_date,
                'date_maturity': line.date_maturity,
                'amount_due': line.amount_residual,
                'overdue': line.date_maturity < today,
            })
        return True

    def action_create_dunning(self):
        self.ensure_one()
        level = self.env['sf.debt.dunning'].search([
            ('active', '=', True),
        ], order='sequence asc, id asc', limit=1)
        if not level:
            raise ValidationError(
                _('No active dunning plan. Create one in '
                  'Configuration > Dunning Plans.'))
        self.env['sf.debt.dunning.run'].create({
            'case_id': self.id,
            'level_id': level.id,
            'partner_id': self.partner_id.id,
            'amount_due': self.total_due,
            'state': 'draft',
        })
        return True


class DebtInvoiceLine(models.Model):
    _name = 'sf.debt.invoice.line'
    _description = 'Overdue Invoice Line'
    _order = 'date_maturity asc, id asc'

    case_id = fields.Many2one(
        'sf.debt.collection.case',
        string='Case',
        required=True,
        ondelete='cascade',
    )
    move_line_id = fields.Many2one(
        'account.move.line',
        string='Journal Item',
        ondelete='set null',
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        ondelete='set null',
    )
    invoice_number = fields.Char(string='Invoice Number')
    date_invoice = fields.Date(string='Invoice Date')
    date_maturity = fields.Date(string='Maturity Date')
    amount_due = fields.Monetary(
        string='Amount Due',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='case_id.currency_id',
        readonly=True,
    )
    overdue = fields.Boolean(string='Overdue', default=False)


class DebtAction(models.Model):
    _name = 'sf.debt.action'
    _description = 'Collection Action'
    _order = 'date desc, id desc'

    case_id = fields.Many2one(
        'sf.debt.collection.case',
        string='Case',
        required=True,
        ondelete='cascade',
    )
    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        required=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        required=True,
    )
    action_type = fields.Selection(
        [
            ('call', 'Phone call'),
            ('email', 'Email'),
            ('letter', 'Letter'),
            ('meeting', 'Meeting'),
            ('note', 'Note'),
        ],
        string='Type',
        required=True,
    )
    summary = fields.Text(string='Summary', required=True)


class DebtPromise(models.Model):
    _name = 'sf.debt.promise'
    _description = 'Payment Promise'
    _order = 'date asc, id asc'

    case_id = fields.Many2one(
        'sf.debt.collection.case',
        string='Case',
        required=True,
        ondelete='cascade',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='case_id.partner_id',
        store=True,
    )
    date = fields.Date(string='Promise Date', required=True)
    amount = fields.Monetary(
        string='Amount',
        currency_field='currency_id',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='case_id.currency_id',
        readonly=True,
    )
    state = fields.Selection(
        [
            ('pending', 'Pending'),
            ('kept', 'Kept'),
            ('broken', 'Broken'),
        ],
        string='Status',
        default='pending',
        required=True,
    )
    note = fields.Text(string='Notes')


class DebtDunningLevel(models.Model):
    _name = 'sf.debt.dunning'
    _description = 'Dunning Level'
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Level Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)
    days_after_due = fields.Integer(
        string='Days After Due',
        default=0,
        help='Send this level this many days after the due date.',
    )
    message = fields.Text(string='Message Template')


class DebtDunningRun(models.Model):
    _name = 'sf.debt.dunning.run'
    _description = 'Dunning Run'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False)
    case_id = fields.Many2one(
        'sf.debt.collection.case',
        string='Case',
        ondelete='cascade',
    )
    partner_id = fields.Many2one('res.partner', string='Customer')
    level_id = fields.Many2one('sf.debt.dunning', string='Dunning Level')
    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
    )
    amount_due = fields.Monetary(
        string='Amount Due',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='case_id.currency_id',
        readonly=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('done', 'Done'),
        ],
        string='Status',
        default='draft',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.debt.dunning.run')
        return super().create(vals_list)

    def action_sent(self):
        self.write({'state': 'sent'})

    def action_done(self):
        self.write({'state': 'done'})