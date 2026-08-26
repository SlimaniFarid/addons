# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_usage = fields.Monetary(
        string='Credit Used',
        currency_field='currency_id',
        compute='_compute_credit_usage',
    )
    credit_available = fields.Monetary(
        string='Credit Available',
        currency_field='currency_id',
        compute='_compute_credit_usage',
    )
    overdue_amount = fields.Monetary(
        string='Overdue Amount',
        currency_field='currency_id',
        compute='_compute_credit_usage',
    )

    def _compute_credit_usage(self):
        today = fields.Date.context_today(self)
        for partner in self:
            lines = self.env['account.move.line'].search([
                ('partner_id', '=', partner.id),
                ('account_id.account_type', '=', 'asset_receivable'),
                ('move_id.state', '=', 'posted'),
                ('amount_residual', '>', 0),
            ])
            usage = sum(lines.mapped('amount_residual'))
            overdue = sum(
                line.amount_residual for line in lines
                if line.date_maturity and line.date_maturity < today)
            partner.credit_usage = usage
            partner.overdue_amount = overdue
            partner.credit_available = (partner.credit_limit or 0) - usage


# --- wave2 ---
class _Wave2Debt(models.Model):
    _inherit = 'sf.debt.collection.case'

    def action_load_overdue_invoices(self):
        """Fill case lines from the partner's really overdue invoices and
        refresh totals / max ageing."""
        self.ensure_one()
        Line = self.env['sf.debt.invoice.line']
        Line.search([('case_id', '=', self.id)]).unlink()
        today = fields.Date.context_today(self)
        moves = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'in', ('not_paid', 'partial')),
            ('partner_id', '=', self.partner_id.id),
        ], order='invoice_date_due asc')
        created = 0
        worst = 0
        for mv in moves:
            overdue_days = (today - mv.invoice_date_due).days
            if overdue_days <= 0 or not mv.amount_residual:
                continue
            Line.create({
                'case_id': self.id,
                'invoice_id': mv.id,
                'due_date': mv.invoice_date_due,
                'overdue_days': overdue_days,
                'amount_residual': mv.amount_residual,
            })
            worst = max(worst, overdue_days)
            created += 1
        self.write({
            'total_due': sum(moves.mapped('amount_total')),
            'total_overdue': sum(Line.search([
                ('case_id', '=', self.id)]).mapped('amount_residual')),
            'days_overdue': worst,
        })
        self.message_post(body=_('Loaded %s overdue invoice(s); '
                                 'worst ageing %s days.') % (created, worst))
        return True


class DebtInvoiceLine(models.Model):
    _name = 'sf.debt.invoice.line'
    _description = 'Debt Case Invoice Detail'

    case_id = fields.Many2one('sf.debt.collection.case', required=True,
                              ondelete='cascade')
    invoice_id = fields.Many2one('account.move', string='Invoice',
                                 ondelete='cascade')
    due_date = fields.Date(string='Due Date')
    overdue_days = fields.Integer(string='Days Overdue')
    amount_residual = fields.Monetary(string='Open Amount',
                                      currency_field='currency_id')
    currency_id = fields.Many2one(related='case_id.currency_id')
