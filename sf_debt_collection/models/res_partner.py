# -*- coding: utf-8 -*-
from odoo import fields, models


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