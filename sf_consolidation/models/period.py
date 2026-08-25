# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ConsolidationPeriod(models.Model):
    _name = 'sf.consolidation.period'
    _description = 'Consolidation Period'
    _rec_name = 'name'
    _order = 'date_from desc'

    name = fields.Char(string='Name', required=True)
    group_id = fields.Many2one('sf.consolidation.group', string='Group',
                               required=True, ondelete='cascade')
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft')
    line_ids = fields.One2many('sf.consolidation.line', 'period_id',
                               string='Lines')
    total_balance = fields.Float(string='Total Balance',
                                 compute='_compute_totals', store=True)

    @api.depends('line_ids.amount')
    def _compute_totals(self):
        for period in self:
            period.total_balance = sum(period.line_ids.mapped('amount'))

    def action_done(self):
        for period in self:
            period.state = 'done'

    def action_generate_from_moves(self):
        """Generate lines from confirmed account moves of the group."""
        self.ensure_one()
        MoveLine = self.env['account.move.line']
        companies = self.group_id.company_ids
        if not companies:
            return
        lines = []
        for company in companies:
            moves = self.env['account.move'].search([
                ('company_id', '=', company.id),
                ('state', '=', 'posted'),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
            ])
            if not moves:
                continue
            move_lines = MoveLine.search([
                ('move_id', 'in', moves.ids),
                ('account_id', '!=', False),
            ])
            for ml in move_lines:
                amount = ml.balance
                if amount == 0.0:
                    continue
                lines.append((0, 0, {
                    'period_id': self.id,
                    'company_id': company.id,
                    'account_id': ml.account_id.id,
                    'amount': amount,
                }))
        if lines:
            self.line_ids = lines

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.consolidation.group'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

