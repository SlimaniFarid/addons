# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfTradeProgram(models.Model):
    _name = 'sf.trade.program'
    _description = 'Trade Promotion Program'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.trade.promotions.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_ids = fields.Many2many(
        'res.partner', string='Eligible Customers',
        domain="[('company_id', 'in', [company_id, False])]"
    )
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    budget = fields.Monetary(string='Budget', required=True, currency_field='currency_id')
    promotion_type = fields.Selection([
        ('invoice_discount', 'Invoice Discount'),
        ('volume_bonus', 'Volume Bonus'),
        ('cash_discount', 'Cash Discount'),
        ('allowance', 'Allowance'),
    ], string='Promotion Type', default='invoice_discount', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    claim_ids = fields.One2many('sf.trade.claim', 'program_id', string='Claims')
    claim_count = fields.Integer(string='Claim Count', compute='_compute_claim_count')
    total_claimed = fields.Monetary(string='Total Claimed', currency_field='currency_id',
                                    compute='_compute_amounts', store=True)
    remaining_budget = fields.Monetary(string='Remaining Budget', currency_field='currency_id',
                                       compute='_compute_amounts', store=True)
    roi = fields.Float(string='ROI (%)', compute='_compute_amounts', digits=(16, 2))
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company, index=True)

    _sql_constraints = [
        ('budget_positive', 'CHECK (budget > 0)', 'The budget must be positive.'),
    ]

    @api.depends('claim_ids.state', 'claim_ids.amount', 'budget')
    def _compute_amounts(self):
        for program in self:
            claims = program.claim_ids.filtered(lambda c: c.state in ('approved', 'paid'))
            program.total_claimed = sum(claims.mapped('amount'))
            program.remaining_budget = program.budget - program.total_claimed
            program.roi = program.budget and \
                round(program.total_claimed * 100.0 / program.budget, 2) or 0.0

    def _close_expired_programs(self):
        """Close expired programs without manager check - for cron usage."""
        for program in self:
            if program.state != 'active':
                raise UserError(_('Only active programs can be closed.'))
            program.state = 'closed'
            program.message_post(body=_('The trade program was closed automatically by cron.'))

    def _cron_daily_checks(self):
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            expired = scoped.env['sf.trade.program'].search([
                ('state', '=', 'active'),
                ('end_date', '<', today),
            ])
            expired.sudo()._close_expired_programs()

    @api.depends('claim_ids')
    def _compute_claim_count(self):
        for program in self:
            program.claim_count = len(program.claim_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.trade.program')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_trade_promotions.group_sf_trade_promotions_manager'):
            raise UserError(_('Only a trade promotions manager can perform this action.'))

    def action_activate(self):
        for program in self:
            if program.state != 'draft':
                raise UserError(_('Only draft programs can be activated.'))
            if program.start_date and program.end_date and program.start_date > program.end_date:
                raise UserError(_('The start date must be before or on the end date.'))
            program.state = 'active'
            program.message_post(body=_('The trade program was activated.'))

    def action_close(self):
        self._check_manager()
        for program in self:
            if program.state != 'active':
                raise UserError(_('Only active programs can be closed.'))
            program.state = 'closed'
            program.message_post(body=_('The trade program was closed.'))

    def action_cancel(self):
        self._check_manager()
        for program in self:
            if program.state not in ('draft', 'active'):
                raise UserError(_('Only draft or active programs can be cancelled.'))
            program.state = 'cancelled'
            program.message_post(body=_('The trade program was cancelled.'))