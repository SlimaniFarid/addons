# -*- coding: utf-8 -*-
"""FX exposure snapshots and forward contracts."""
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFxExposure(models.Model):
    _name = 'sf.fx.exposure'
    _description = 'FX Exposure Snapshot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'snapshot_date desc'

    name = fields.Char(string='Snapshot', required=True, copy=False,
                       readonly=True, default='New')
    snapshot_date = fields.Date(string='Snapshot Date', required=True,
                                default=fields.Date.today)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    line_ids = fields.One2many('sf.fx.exposure.line', 'exposure_id',
                               string='Currency Positions')
    state = fields.Selection([
        ('draft', 'Draft'), ('computed', 'Computed')], default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.fx.exposure') or 'FXEXP-NEW'
        return super().create(vals_list)

    def action_compute(self):
        self.ensure_one()
        self.line_ids.unlink()
        company = self.company_id
        items = self.env['account.move.line'].search([
            ('move_id.state', '=', 'posted'),
            ('company_id', '=', company.id),
            ('currency_id', '!=', False),
            ('currency_id', '!=', company.currency_id.id),
            ('account_id.account_type', 'in',
             ('asset_receivable', 'liability_payable')),
            ('reconciled', '=', False),
        ])
        positions = defaultdict(float)
        for item in items:
            signed = item.amount_currency
            positions[item.currency_id.id] += signed
        vals_list = []
        for currency_id, amount in positions.items():
            if abs(amount) < 0.005:
                continue
            currency = self.env['res.currency'].browse(currency_id)
            hedged = sum(
                h.notional for h in self.env['sf.fx.hedge'].search([
                    ('company_id', '=', company.id),
                    ('currency_id', '=', currency_id),
                    ('state', 'in', ('active', 'settled')),
                    ('direction', '=',
                     'sell' if amount > 0 else 'buy'),
                ]))
            vals_list.append({
                'exposure_id': self.id,
                'currency_id': currency_id,
                'net_open_amount': amount,
                'hedged_amount': hedged,
                'coverage_percent': (hedged / abs(amount) * 100.0)
                if amount else 0.0,
            })
        if vals_list:
            self.env['sf.fx.exposure.line'].create(vals_list)
        self.write({'state': 'computed'})


class SfFxExposureLine(models.Model):
    _name = 'sf.fx.exposure.line'
    _description = 'FX Exposure Position'

    exposure_id = fields.Many2one('sf.fx.exposure', required=True,
                                  ondelete='cascade')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True)
    net_open_amount = fields.Float(string='Net Open Position')
    hedged_amount = fields.Float(string='Hedged (forwards)')
    coverage_percent = fields.Float(string='Coverage %')


class SfFxHedge(models.Model):
    _name = 'sf.fx.hedge'
    _description = 'FX Forward Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'value_date desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True,
                                  help='Foreign currency bought or sold.')
    counterparty_bank_id = fields.Many2one('res.partner',
                                           string='Counterparty Bank')
    direction = fields.Selection([
        ('buy', 'Buy Foreign Currency'),
        ('sell', 'Sell Foreign Currency')], required=True,
        default='buy')
    notional = fields.Float(string='Notional Amount', required=True)
    strike_rate = fields.Float(string='Forward Rate', required=True)
    trade_date = fields.Date(string='Trade Date', required=True,
                             default=fields.Date.today)
    value_date = fields.Date(string='Value Date (Maturity)', required=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('active', 'Active'), ('settled', 'Settled'),
        ('cancelled', 'Cancelled')], default='draft', tracking=True)
    spot_rate_at_settlement = fields.Float(string='Spot Rate at Settlement',
                                           readonly=True)
    settlement_gain_loss = fields.Float(string='Realized Gain/(Loss)',
                                        readonly=True)
    settlement_date = fields.Date(string='Settled On', readonly=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.fx.hedge') or 'FXH-NEW'
        return super().create(vals_list)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_settle(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active hedges can be settled.'))
        company = self.company_id
        currency = self.currency_id
        spot = currency.with_company(company)._get_conversion_rate(
            currency, company.currency_id,
            fields.Date.context_today(self))
        self.spot_rate_at_settlement = spot
        if self.direction == 'buy':
            self.settlement_gain_loss = self.notional * (
                spot - self.strike_rate)
        else:
            self.settlement_gain_loss = self.notional * (
                self.strike_rate - spot)
        self.write({'state': 'settled',
                    'settlement_date': fields.Date.context_today(self)})
