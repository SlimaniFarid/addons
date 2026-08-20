# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class InvestPortfolio(models.Model):
    _name = 'sf.invest.portfolio'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Investment Portfolio'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    company_account = fields.Char(string='Company account')
    bank = fields.Char(string='Bank')
    currency = fields.Char(string='Currency', default='EUR')
    responsible_id = fields.Many2one('res.users', string='Responsible',
                                     ondelete='restrict')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    line_ids = fields.One2many('sf.invest.line', 'portfolio_id',
                               string='Investment lines')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.invest.portfolio')
            vals['name'] = seq
        return super().create(vals)

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft portfolios can be opened.'))
        self.state = 'open'

    def action_close(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_investment_management.group_invest_manager'):
            raise UserError(_('Only investment managers can close a '
                              'portfolio.'))
        if self.state != 'open':
            raise UserError(_('Only open portfolios can be closed.'))
        self.state = 'closed'


class InvestLine(models.Model):
    _name = 'sf.invest.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Investment Line'
    _order = 'security_name'

    name = fields.Char(string='Number', required=True, index=True)
    portfolio_id = fields.Many2one('sf.invest.portfolio',
                                   string='Portfolio', required=True,
                                   ondelete='cascade', index=True)
    security_type = fields.Selection([
        ('stock', 'Stock'),
        ('bond', 'Bond'),
        ('money_market', 'Money Market'),
        ('term_deposit', 'Term Deposit'),
        ('other', 'Other'),
    ], string='Security type', required=True)
    security_name = fields.Char(string='Security name', required=True)
    isin = fields.Char(string='ISIN')
    quantity = fields.Float(string='Quantity', required=True, default=0.0)
    cost_price = fields.Float(string='Cost price', required=True,
                              default=0.0)
    current_price = fields.Float(string='Current price', required=True,
                                 default=0.0)
    value = fields.Float(string='Value', compute='_compute_value',
                         store=True)
    latent_gain = fields.Float(string='Latent gain/loss',
                               compute='_compute_value', store=True)
    maturity_date = fields.Date(string='Maturity date')
    coupon_rate = fields.Float(string='Coupon rate')
    coupon_expected = fields.Float(string='Expected coupon',
                                   compute='_compute_coupon', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('matured', 'Matured'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    valuation_ids = fields.One2many('sf.invest.valuation', 'line_id',
                                    string='Valuations')
    income_ids = fields.One2many('sf.invest.income', 'line_id',
                                 string='Incomes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('quantity', 'current_price', 'cost_price')
    def _compute_value(self):
        for line in self:
            line.value = line.quantity * line.current_price
            line.latent_gain = (line.current_price - line.cost_price) \
                * line.quantity

    @api.depends('quantity', 'coupon_rate')
    def _compute_coupon(self):
        for line in self:
            line.coupon_expected = line.quantity * line.coupon_rate

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.invest.line')
            vals['name'] = seq
        return super().create(vals)

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft investment lines can be opened.'))
        self.state = 'open'

    def action_mark_matured(self):
        self.ensure_one()
        if self.state not in ('open', 'draft'):
            raise UserError(_('Only open investment lines can be marked as '
                              'matured.'))
        self.state = 'matured'

    def action_close(self):
        self.ensure_one()
        if self.state not in ('open', 'matured'):
            raise UserError(_('Only open or matured investment lines can be '
                              'closed.'))
        self.state = 'closed'

    def action_generate_coupon_income(self):
        self.ensure_one()
        if not self.coupon_expected:
            raise UserError(_('No expected coupon for this investment '
                              'line.'))
        income = self.env['sf.invest.income'].create({
            'line_id': self.id,
            'income_type': 'coupon',
            'amount': self.coupon_expected,
            'date': fields.Date.context_today(self),
        })
        return {
            'name': _('Coupon Income'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.invest.income',
            'view_mode': 'form',
            'res_id': income.id,
        }

    def _check_invest_alerts(self):
        activity_todo = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            today = fields.Date.context_today(self.with_company(company))
            lines = self.with_company(company).search([
                ('security_type', 'in', ('bond', 'term_deposit')),
                ('state', '=', 'open'),
                ('maturity_date', '!=', False),
                ('company_id', '=', company.id),
            ])
            for rec in lines:
                if rec.maturity_date < today:
                    rec.state = 'matured'
                    continue
                alert_days = rec.company_id.sf_invest_alert_days or 0
                if rec.maturity_date - timedelta(days=alert_days) <= today:
                    existing = rec.activity_ids.filtered(
                        lambda a: a.activity_type_id == activity_todo
                        and a.state != 'done')
                    if existing:
                        continue
                    rec.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Maturity approaching: %s')
                        % rec.security_name,
                        note=_('The %(type)s line %(name)s matures on %(date)s.')
                        % {'type': rec.security_type,
                           'name': rec.security_name,
                           'date': rec.maturity_date},
                        user_id=rec.portfolio_id.responsible_id.id
                        if rec.portfolio_id.responsible_id else self.env.user.id)


class InvestValuation(models.Model):
    _name = 'sf.invest.valuation'
    _description = 'Investment Valuation'
    _order = 'date desc, id desc'

    name = fields.Char(string='Number', required=True, index=True)
    line_id = fields.Many2one('sf.invest.line', string='Investment line',
                              required=True, ondelete='cascade', index=True)
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today)
    price = fields.Float(string='Market price', required=True, default=0.0)
    computed_value = fields.Float(string='Computed value',
                                  compute='_compute_computed_value',
                                  store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='line_id.company_id', store=True,
                                 readonly=True)

    @api.depends('line_id.quantity', 'price')
    def _compute_computed_value(self):
        for val in self:
            val.computed_value = val.line_id.quantity * val.price

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.invest.valuation')
            vals['name'] = seq
        return super().create(vals)


class InvestIncome(models.Model):
    _name = 'sf.invest.income'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Investment Income'
    _order = 'date desc, id desc'

    name = fields.Char(string='Number', required=True, index=True)
    line_id = fields.Many2one('sf.invest.line', string='Investment line',
                              required=True, ondelete='cascade', index=True)
    income_type = fields.Selection([
        ('dividend', 'Dividend'),
        ('coupon', 'Coupon'),
        ('interest', 'Interest'),
        ('other', 'Other'),
    ], string='Income type', required=True)
    amount = fields.Float(string='Amount', required=True, default=0.0)
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today)
    reference = fields.Char(string='Reference')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='line_id.company_id', store=True,
                                 readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.invest.income')
            vals['name'] = seq
        return super().create(vals)

    def action_received(self):
        if not self.env.user.has_group(
                'sf_investment_management.group_invest_manager'):
            raise UserError(_('Only investment managers can validate income '
                              'receipts.'))
        for rec in self:
            if rec.income_type == 'coupon' and not rec.amount:
                rec.amount = rec.line_id.quantity * rec.line_id.coupon_rate
            if rec.state == 'draft':
                rec.state = 'received'

    def action_close(self):
        self.ensure_one()
        if self.state != 'received':
            raise UserError(_('Only received incomes can be closed.'))
        self.state = 'closed'