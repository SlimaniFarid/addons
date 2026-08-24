# -*- coding: utf-8 -*-
"""Customer rebate deals (sell-side)."""
import dateutil.relativedelta as rd

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomerRebateDeal(models.Model):
    _name = 'sf.customer.rebate.deal'
    _description = 'Customer Rebate Deal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end desc'

    name = fields.Char(string='Deal Reference', required=True, copy=False,
                       readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True,
                                 domain=[('customer_rank', '>', 0)])
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    date_start = fields.Date(string='Period Start', required=True)
    date_end = fields.Date(string='Period End', required=True)
    deal_type = fields.Selection([
        ('retro_percent', 'Retro % on Sales'),
        ('turnover_bonus', 'Turnover Bonus'),
        ('per_unit', 'Fixed per Unit')], required=True,
        default='retro_percent')
    product_category_id = fields.Many2one('product.category',
                                          string='Category Scope')
    threshold_amount = fields.Monetary(string='Sales Threshold')
    rebate_percent = fields.Float(string='Rebate %')
    rebate_per_unit = fields.Monetary(string='Rebate per Unit')
    fixed_bonus_amount = fields.Monetary(string='Fixed Bonus')
    state = fields.Selection([
        ('draft', 'Draft'), ('active', 'Active'), ('settled', 'Settled'),
        ('expired', 'Expired')], default='draft', tracking=True)
    accrual_ids = fields.One2many('sf.customer.rebate.accrual', 'deal_id',
                                  string='Accruals')
    total_sales = fields.Float(compute='_compute_totals')
    total_accrued = fields.Float(compute='_compute_totals')
    credit_note_ref = fields.Char(string='Settlement Credit Note Ref')
    settled_date = fields.Date(string='Settled On', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.rebate.deal') or 'CRB-NEW'
        return super().create(vals_list)

    def _compute_totals(self):
        for deal in self:
            invoices = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                ('partner_id', '=', deal.partner_id.id),
                ('invoice_date', '>=', deal.date_start),
                ('invoice_date', '<=', deal.date_end),
                ('company_id', '=', deal.company_id.id)])
            sales = 0.0
            for inv in invoices:
                for line in inv.invoice_line_ids.filtered(
                        lambda l: not l.display_type):
                    if (deal.product_category_id and line.product_id.categ_id
                            != deal.product_category_id):
                        continue
                    sales += line.price_subtotal
            deal.total_sales = sales
            deal.total_accrued = sum(a.accrued_amount
                                     for a in deal.accrual_ids)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_expire(self):
        self.write({'state': 'expired'})

    def action_compute_accrual(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active deals can compute accruals.'))
        self.accrual_ids.filtered(lambda a: not a.claimed).unlink()
        current = self.date_start.replace(day=1)
        vals_list = []
        while current <= self.date_end:
            month_end = current + rd.relativedelta(months=1, days=-1)
            invoices = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                ('partner_id', '=', self.partner_id.id),
                ('invoice_date', '>=', current),
                ('invoice_date', '<=', min(month_end, self.date_end)),
                ('company_id', '=', self.company_id.id)])
            sales, units = 0.0, 0.0
            for inv in invoices:
                for line in inv.invoice_line_ids.filtered(
                        lambda l: not l.display_type):
                    if (self.product_category_id
                            and line.product_id.categ_id
                            != self.product_category_id):
                        continue
                    sales += line.price_subtotal
                    units += line.quantity
            if self.deal_type == 'retro_percent':
                amount = sales * self.rebate_percent / 100.0
            elif self.deal_type == 'per_unit':
                amount = units * self.rebate_per_unit
            else:
                amount = 0.0
            vals_list.append({
                'deal_id': self.id, 'period_month': current,
                'sales': sales, 'units': units, 'accrued_amount': amount})
            current += rd.relativedelta(months=1)
        if vals_list:
            self.env['sf.customer.rebate.accrual'].create(vals_list)

    def action_settle(self):
        self.ensure_one()
        if not self.credit_note_ref:
            raise UserError(_('Enter the settlement credit note reference.'))
        self.write({'state': 'settled',
                    'settled_date': fields.Date.today()})


class SfCustomerRebateAccrual(models.Model):
    _name = 'sf.customer.rebate.accrual'
    _description = 'Customer Rebate Accrual'

    deal_id = fields.Many2one('sf.customer.rebate.deal', required=True,
                              ondelete='cascade')
    company_id = fields.Many2one(related='deal_id.company_id', store=True)
    currency_id = fields.Many2one(related='deal_id.currency_id')
    period_month = fields.Date(string='Month')
    sales = fields.Float(string='Sales')
    units = fields.Float(string='Units')
    accrued_amount = fields.Float(string='Accrued Rebate')
    claimed = fields.Boolean(default=False)
