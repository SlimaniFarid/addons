# -*- coding: utf-8 -*-
"""Monthly management report pack."""
import dateutil.relativedelta as rd

from odoo import api, fields, models, _


class SfMgmtReport(models.Model):
    _name = 'sf.mgmt.report'
    _description = 'Monthly Management Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'period_start desc'

    name = fields.Char(string='Report', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    period_start = fields.Date(string='Month Start', required=True)
    period_end = fields.Date(string='Month End', required=True)
    revenue = fields.Float(string='Revenue', readonly=True)
    costs = fields.Float(string='Vendor Costs', readonly=True)
    gross_margin = fields.Float(string='Gross Margin', readonly=True)
    margin_percent = fields.Float(string='Margin %', readonly=True)
    prev_revenue = fields.Float(string='Prev Month Revenue', readonly=True)
    revenue_delta_percent = fields.Float(string='Revenue Delta %',
                                         readonly=True)
    invoice_count = fields.Integer(string='Customer Invoices', readonly=True)
    line_ids = fields.One2many('sf.mgmt.report.kpi', 'report_id',
                               string='KPI Lines')
    commentary = fields.Html(string='Executive Commentary')
    state = fields.Selection([
        ('draft', 'Draft'), ('computed', 'Computed'), ('final', 'Final')],
        default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.mgmt.report') or 'MRP-NEW'
        return super().create(vals_list)

    def action_compute(self):
        self.ensure_one()
        company = self.company_id
        inv_domain = [('move_type', '=', 'out_invoice'),
                      ('state', '=', 'posted'),
                      ('invoice_date', '>=', self.period_start),
                      ('invoice_date', '<=', self.period_end),
                      ('company_id', '=', company.id)]
        bill_domain = [('move_type', '=', 'in_invoice'),
                       ('state', '=', 'posted'),
                       ('invoice_date', '>=', self.period_start),
                       ('invoice_date', '<=', self.period_end),
                       ('company_id', '=', company.id)]
        invoices = self.env['account.move'].search(inv_domain)
        bills = self.env['account.move'].search(bill_domain)
        prev_start = self.period_start - rd.relativedelta(months=1)
        prev_end = self.period_start - rd.relativedelta(days=1)
        prev_invoices = self.env['account.move'].search([
            inv_domain[0], inv_domain[1], inv_domain[5], inv_domain[6],
            ('invoice_date', '>=', prev_start),
            ('invoice_date', '<=', prev_end),
            ('company_id', '=', company.id)])
        revenue = sum(invoices.mapped('amount_untaxed'))
        costs = sum(bills.mapped('amount_untaxed'))
        prev_rev = sum(prev_invoices.mapped('amount_untaxed'))
        margin = revenue - costs
        self.write({
            'revenue': revenue,
            'costs': costs,
            'gross_margin': margin,
            'margin_percent': (margin / revenue * 100.0) if revenue else 0.0,
            'prev_revenue': prev_rev,
            'revenue_delta_percent': ((revenue - prev_rev) / prev_rev * 100.0)
            if prev_rev else 0.0,
            'invoice_count': len(invoices),
            'state': 'computed'})

    def action_finalize(self):
        self.write({'state': 'final'})


class SfMgmtReportKpi(models.Model):
    _name = 'sf.mgmt.report.kpi'
    _description = 'Management Report KPI'

    report_id = fields.Many2one('sf.mgmt.report', required=True,
                                ondelete='cascade')
    company_id = fields.Many2one(related='report_id.company_id', store=True)
    currency_id = fields.Many2one(related='report_id.currency_id')
    name = fields.Char(string='KPI', required=True)
    value = fields.Float(string='Value')
    previous_value = fields.Float(string='Previous')
    delta_percent = fields.Float(string='Delta %',
                                 compute='_compute_delta')
    comment = fields.Char(string='Comment')

    @api.depends('value', 'previous_value')
    def _compute_delta(self):
        for rec in self:
            rec.delta_percent = ((rec.value - rec.previous_value) /
                                 rec.previous_value * 100.0
                                 if rec.previous_value else 0.0)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.mgmt.report'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
