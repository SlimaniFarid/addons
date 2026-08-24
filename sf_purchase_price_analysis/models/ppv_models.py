# -*- coding: utf-8 -*-
"""Purchase price variance analysis."""
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPpvAnalysis(models.Model):
    _name = 'sf.ppv.analysis'
    _description = 'Purchase Price Variance Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end desc'

    name = fields.Char(string='Analysis', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    date_start = fields.Date(string='From', required=True)
    date_end = fields.Date(string='To', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor Filter',
                                domain=[('supplier_rank', '>', 0)])
    tolerance_percent = fields.Float(string='Alert Tolerance %', default=5.0)
    line_ids = fields.One2many('sf.ppv.line', 'analysis_id',
                               string='PPV Lines')
    total_variance = fields.Float(compute='_compute_totals')
    alert_count = fields.Integer(compute='_compute_totals')
    state = fields.Selection([('draft', 'Draft'), ('computed', 'Computed')],
                             default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.ppv.analysis') or 'PPV-NEW'
        return super().create(vals_list)

    def _compute_totals(self):
        for rec in self:
            rec.total_variance = sum(l.variance_amount for l in rec.line_ids)
            rec.alert_count = len(rec.line_ids.filtered('alert'))

    def action_compute(self):
        self.ensure_one()
        self.line_ids.unlink()
        domain = [
            ('move_type', '=', 'in_invoice'), ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_start),
            ('invoice_date', '<=', self.date_end),
            ('company_id', '=', self.company_id.id),
        ]
        if self.vendor_id:
            domain.append(('partner_id', '=', self.vendor_id.id))
        invoices = self.env['account.move'].search(domain)
        buckets = defaultdict(lambda: {'qty': 0.0, 'total': 0.0,
                                       'vendor': False})
        for inv in invoices:
            for line in inv.invoice_line_ids.filtered(
                    lambda l: not l.display_type and l.product_id):
                key = (line.product_id.id, inv.partner_id.id)
                buckets[key]['qty'] += line.quantity
                buckets[key]['total'] += line.price_subtotal
                buckets[key]['vendor'] = inv.partner_id.id
        vals_list = []
        for (product_id, vendor_id), data in buckets.items():
            if data['qty'] <= 0:
                continue
            product = self.env['product.product'].browse(product_id)
            actual = data['total'] / data['qty']
            standard = product.standard_price or 0.0
            variance_amount = (actual - standard) * data['qty']
            variance_percent = ((actual - standard) / standard * 100.0
                                if standard else 0.0)
            vals_list.append({
                'analysis_id': self.id,
                'product_id': product_id,
                'vendor_id': vendor_id,
                'quantity': data['qty'],
                'actual_unit_price': actual,
                'standard_cost': standard,
                'variance_amount': variance_amount,
                'variance_percent': variance_percent,
                'alert': abs(variance_percent) > self.tolerance_percent,
            })
        if vals_list:
            self.env['sf.ppv.line'].create(vals_list)
        self.write({'state': 'computed'})


class SfPpvLine(models.Model):
    _name = 'sf.ppv.line'
    _description = 'PPV Line'

    analysis_id = fields.Many2one('sf.ppv.analysis', required=True,
                                  ondelete='cascade')
    company_id = fields.Many2one(related='analysis_id.company_id', store=True)
    currency_id = fields.Many2one(related='analysis_id.currency_id')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    quantity = fields.Float(string='Qty Purchased')
    actual_unit_price = fields.Float(string='Actual Avg Price')
    standard_cost = fields.Float(string='Standard Cost')
    variance_amount = fields.Float(string='Variance Amount')
    variance_percent = fields.Float(string='Variance %')
    alert = fields.Boolean(string='Alert')
