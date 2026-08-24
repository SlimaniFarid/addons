# -*- coding: utf-8 -*-
"""Lease modifications and reassessments (IFRS 16 para 44-46)."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLeaseModification(models.Model):
    """Re-measurement event: modification, reassessment or impairment review."""
    _name = 'sf.lease.modification'
    _description = 'Lease Modification / Reassessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'effective_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    contract_id = fields.Many2one('sf.lease.contract', string='Lease Contract',
                                  required=True, ondelete='cascade')
    company_id = fields.Many2one(related='contract_id.company_id', store=True)
    currency_id = fields.Many2one(related='contract_id.currency_id')
    mod_type = fields.Selection([
        ('modification', 'Contract Modification'),
        ('reassessment', 'Reassessment (index / residual value)'),
        ('impairment_indicator', 'Impairment Indicator Review'),
    ], string='Type', required=True, default='modification', tracking=True)
    effective_date = fields.Date(string='Effective Date', required=True,
                                 default=fields.Date.today)
    reason = fields.Text(string='Reason / Description', required=True)

    new_payment_amount = fields.Monetary(string='New Payment per Period')
    new_term_months = fields.Integer(string='New Total Term (months)')
    new_ibr = fields.Float(string='New IBR % (annual)')
    extend_term_months = fields.Integer(
        string='Extend Term By (months)',
        help='Alternative to new total term: adds months to current term.')

    remeasured_liability = fields.Monetary(string='Re-measured Liability',
                                           readonly=True)
    liability_before = fields.Monetary(string='Liability Before', readonly=True)
    adjustment = fields.Monetary(string='ROU Adjustment', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('applied', 'Applied'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.lease.modification') or 'LMOD-NEW'
        return super().create(vals_list)

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_apply(self):
        """Re-measure remaining liability and adjust the ROU asset."""
        for mod in self:
            contract = mod.contract_id
            if contract.state not in ('active', 'modified'):
                raise UserError(_(
                    'Modifications can only be applied to active leases.'))
            unposted = contract.payment_line_ids.filtered(lambda l: not l.posted)
            if not unposted:
                raise UserError(_('No unposted periods remain on this lease.'))

            payment = mod.new_payment_amount or contract.payment_amount
            ibr = mod.new_ibr or contract.incremental_borrowing_rate
            if mod.new_term_months:
                total_term = mod.new_term_months
            elif mod.extend_term_months:
                total_term = contract.term_months + mod.extend_term_months
            else:
                total_term = contract.term_months

            ppy = contract._periods_per_year()
            remaining_periods = max(1, int(round(total_term * ppy / 12.0)))
            rate = ibr / 100.0 / ppy
            pv = 0.0
            for t in range(remaining_periods):
                exponent = t if contract.payment_timing == 'advance' else t + 1
                pv += payment / ((1.0 + rate) ** exponent)
            pv = round(pv, 2)

            first_unposted = min(unposted, key=lambda l: l.sequence)
            liability_before = first_unposted.opening_liability
            adjustment = round(pv - liability_before, 2)

            contract.write({
                'payment_amount': payment,
                'incremental_borrowing_rate': ibr,
                'term_months': total_term,
                'state': 'modified',
            })

            unposted.unlink()
            seq_base = len(contract.payment_line_ids)
            posted_count = seq_base
            rou_base = contract.rou_asset_initial + adjustment
            remaining_total = posted_count + remaining_periods
            liability = pv
            vals_list = []
            for t in range(remaining_periods):
                due = contract._add_period(mod.effective_date, t)
                if contract.payment_timing == 'advance':
                    interest = max(0.0, (liability - payment) * rate)
                else:
                    interest = liability * rate
                principal = payment - interest
                vals_list.append({
                    'contract_id': contract.id,
                    'sequence': seq_base + t + 1,
                    'period_index': seq_base + t + 1,
                    'due_date': due,
                    'payment_amount': payment,
                    'opening_liability': round(liability, 2),
                    'interest': round(interest, 2),
                    'principal': round(principal, 2),
                    'closing_liability': round(liability - principal, 2),
                    'depreciation': round(rou_base / remaining_total, 2)
                    if not contract.is_exempt else 0.0,
                })
                liability -= principal
            self.env['sf.lease.payment.line'].create(vals_list)

            mod.write({
                'state': 'applied',
                'remeasured_liability': pv,
                'liability_before': round(liability_before, 2),
                'adjustment': adjustment,
            })
            contract.message_post(body=_(
                'Modification %s applied: liability re-measured from %s to %s, '
                'ROU adjustment %s.') % (mod.name, round(liability_before, 2),
                                         pv, adjustment))
