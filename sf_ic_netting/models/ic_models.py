# -*- coding: utf-8 -*-
"""Intercompany netting sessions."""
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfIcNettingSession(models.Model):
    _name = 'sf.ic.netting.session'
    _description = 'Intercompany Netting Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Session', required=True, copy=False,
                       readonly=True, default='New')
    period_start = fields.Date(string='From', required=True,
                               default=lambda s: s.env.company.compute_fiscalyear_dates(
                                   fields.Date.today())['date_from'])
    period_end = fields.Date(string='To', required=True,
                             default=fields.Date.today)
    company_ids = fields.Many2many('res.company', string='Participating Entities')
    line_ids = fields.One2many('sf.ic.netting.line', 'session_id',
                               string='Net Positions')
    dispute_ids = fields.One2many('sf.ic.netting.dispute', 'session_id',
                                  string='Disputed Items')
    dispute_count = fields.Integer(compute='_compute_dispute_count')
    total_net = fields.Float(string='Total Net Settled',
                             compute='_compute_total_net')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Computed'),
        ('confirmed', 'Confirmed'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled')],
        default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Session Owner',
                                 required=True, default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    settlement_move_ids = fields.Many2many('account.move', string='Settlement Entries')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.ic.netting') or 'ICNET-NEW'
        return super().create(vals_list)

    def _compute_dispute_count(self):
        for rec in self:
            rec.dispute_count = len(rec.dispute_ids)

    def _compute_total_net(self):
        for rec in self:
            rec.total_net = sum(l.net_amount for l in rec.line_ids)

    def _partner_company_map(self, companies):
        """Map company partner ids to company records."""
        mapping = {}
        for company in companies:
            if company.partner_id:
                mapping[company.partner_id.id] = company
        return mapping

    def action_compute(self):
        self.ensure_one()
        companies = self.company_ids or self.env['res.company'].search([])
        pmap = self._partner_company_map(companies)
        company_ids = companies.ids
        if len(company_ids) < 2:
            raise UserError(_('Select at least two participating entities.'))

        self.line_ids.unlink()
        self.dispute_ids.unlink()
        AccountMoveLine = self.env['account.move.line']
        items = AccountMoveLine.search([
            ('move_id.state', '=', 'posted'),
            ('account_id.account_type', 'in',
             ('asset_receivable', 'liability_payable')),
            ('partner_id', '!=', False),
            ('date', '<=', self.period_end),
            ('company_id', 'in', company_ids),
            ('reconciled', '=', False),
        ])
        buckets = defaultdict(lambda: {'amount': 0.0, 'count': 0,
                                       'items': []})
        for item in items:
            counterpart = pmap.get(item.partner_id.id)
            if not counterpart or counterpart.id == item.company_id.id:
                continue
            if counterpart.id not in company_ids:
                continue
            # signed: receivable positive (they owe us), payable negative
            signed = item.amount_residual
            if item.account_id.account_type == 'liability_payable':
                signed = -item.amount_residual
            key = (item.company_id.id, counterpart.id)
            buckets[key]['amount'] += signed
            buckets[key]['count'] += 1
            buckets[key]['items'].append(item)

        vals_list = []
        for (company_id, counter_id), data in buckets.items():
            vals_list.append({
                'session_id': self.id,
                'company_id': company_id,
                'counterpart_company_id': counter_id,
                'gross_receivable': data['amount'] if data['amount'] > 0 else 0.0,
                'gross_payable': -data['amount'] if data['amount'] < 0 else 0.0,
                'net_amount': data['amount'],
                'item_count': data['count'],
            })
        if vals_list:
            self.env['sf.ic.netting.line'].create(vals_list)
        self.write({'state': 'computed'})

    def action_confirm(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Compute the session first.'))
        self.write({'state': 'confirmed'})

    def action_settle(self):
        """Create a settlement journal entry per net payer company."""
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Confirm the session before settling.'))
        moves = self.env['account.move']
        for line in self.line_ids.filtered(lambda l: abs(l.net_amount) > 0.009):
            move = self.env['account.move'].create({
                'move_type': 'entry',
                'date': fields.Date.context_today(self),
                'ref': _('IC netting %s: %s vs %s') % (
                    self.name, line.company_id.name,
                    line.counterpart_company_id.name),
                'journal_id': self._get_settlement_journal(line.company_id).id,
                'company_id': line.company_id.id,
                'line_ids': [
                    (0, 0, {
                        'name': _('Due from %s') % line.counterpart_company_id.name,
                        'account_id': self._get_due_account(
                            line.company_id, 'from').id,
                        'debit': max(line.net_amount, 0.0),
                        'credit': max(-line.net_amount, 0.0),
                    }),
                    (0, 0, {
                        'name': _('Due to %s') % line.company_id.name,
                        'account_id': self._get_due_account(
                            line.counterpart_company_id, 'to').id,
                        'debit': max(-line.net_amount, 0.0),
                        'credit': max(line.net_amount, 0.0),
                    }),
                ],
            })
            moves |= move
        moves.action_post()
        self.write({'state': 'settled',
                    'settlement_move_ids': [(6, 0, moves.ids)]})

    def _get_settlement_journal(self, company):
        journal = self.env['account.journal'].search([
            ('type', '=', 'general'), ('company_id', '=', company.id)],
            limit=1)
        if not journal:
            raise UserError(_('No general journal found for %s.')
                            % company.name)
        return journal

    def _get_due_account(self, company, direction):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_ic_netting.due_%s_account_id_%s' % (direction, company.id))
        if param:
            return self.env['account.account'].browse(int(param))
        account_type = ('asset_receivable' if direction == 'from'
                        else 'liability_payable')
        account = self.env['account.account'].search(
            [('account_type', '=', account_type),
             ('company_id', '=', company.id)], limit=1)
        return account

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class SfIcNettingLine(models.Model):
    _name = 'sf.ic.netting.line'
    _description = 'IC Netting Position'

    session_id = fields.Many2one('sf.ic.netting.session', required=True,
                                 ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Entity', required=True)
    counterpart_company_id = fields.Many2one('res.company',
                                             string='Counterpart Entity',
                                             required=True)
    currency_id = fields.Many2one(related='session_id.currency_id')
    gross_receivable = fields.Float(string='Gross Receivable')
    gross_payable = fields.Float(string='Gross Payable')
    net_amount = fields.Float(string='Net Position')
    item_count = fields.Integer(string='Open Items')
    settled = fields.Boolean(default=False)


class SfIcNettingDispute(models.Model):
    _name = 'sf.ic.netting.dispute'
    _description = 'IC Disputed Item'

    session_id = fields.Many2one('sf.ic.netting.session', required=True,
                                 ondelete='cascade')
    move_line_id = fields.Many2one('account.move.line', string='Journal Item')
    company_id = fields.Many2one(related='session_id.company_id')
    reason = fields.Text(string='Dispute Reason', required=True)
    state = fields.Selection([
        ('open', 'Open'), ('resolved', 'Resolved')], default='open')
    resolved_notes = fields.Text(string='Resolution')

    def action_resolve(self):
        for rec in self:
            rec.write({'state': 'resolved'})
