# -*- coding: utf-8 -*-
"""Procurement spend analytics."""
from collections import defaultdict

from odoo import api, fields, models, _


class SfSpendAnalysis(models.Model):
    _name = 'sf.spend.analysis'
    _description = 'Spend Analysis Run'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end desc'

    name = fields.Char(string='Analysis', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    date_start = fields.Date(string='From', required=True)
    date_end = fields.Date(string='To', required=True)
    maverick_tolerance = fields.Float(string='Maverick Alert %', default=20.0)
    line_ids = fields.One2many('sf.spend.line', 'analysis_id',
                               string='Spend Lines')
    total_spend = fields.Float(compute='_compute_totals')
    total_maverick = fields.Float(compute='_compute_totals')
    state = fields.Selection([('draft', 'Draft'), ('computed', 'Computed')],
                             default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.spend.analysis') or 'SPND-NEW'
        return super().create(vals_list)

    def _compute_totals(self):
        for rec in self:
            rec.total_spend = sum(l.spend_amount for l in rec.line_ids)
            rec.total_maverick = sum(l.maverick_amount for l in rec.line_ids)

    def action_compute(self):
        self.ensure_one()
        self.line_ids.unlink()
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'in_invoice'), ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_start),
            ('invoice_date', '<=', self.date_end),
            ('company_id', '=', self.company_id.id)])
        buckets = defaultdict(lambda: {'amount': 0.0, 'po': 0.0, 'count': 0,
                                       'category': False})
        for inv in invoices:
            for line in inv.invoice_line_ids.filtered(
                    lambda l: not l.display_type):
                key = inv.partner_id.id
                b = buckets[key]
                b['amount'] += line.price_subtotal
                b['count'] += 1
                if line.purchase_line_id:
                    b['po'] += line.price_subtotal
                if line.product_id.categ_id:
                    b['category'] = line.product_id.categ_id.id
        vals_list = []
        for vendor_id, b in buckets.items():
            maverick = b['amount'] - b['po']
            pct = (maverick / b['amount'] * 100.0) if b['amount'] else 0.0
            vals_list.append({
                'analysis_id': self.id,
                'vendor_id': vendor_id,
                'category_id': b['category'],
                'invoice_count': b['count'],
                'spend_amount': b['amount'],
                'po_covered_amount': b['po'],
                'maverick_amount': maverick,
                'maverick_percent': pct,
                'alert': pct > self.maverick_tolerance,
            })
        if vals_list:
            self.env['sf.spend.line'].create(vals_list)
        self.write({'state': 'computed'})


class SfSpendLine(models.Model):
    _name = 'sf.spend.line'
    _description = 'Spend Line'

    analysis_id = fields.Many2one('sf.spend.analysis', required=True,
                                  ondelete='cascade')
    company_id = fields.Many2one(related='analysis_id.company_id', store=True)
    currency_id = fields.Many2one(related='analysis_id.currency_id')
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    category_id = fields.Many2one('product.category', string='Main Category')
    invoice_count = fields.Integer(string='Bills')
    spend_amount = fields.Float(string='Spend')
    po_covered_amount = fields.Float(string='PO-Covered')
    maverick_amount = fields.Float(string='Maverick Spend')
    maverick_percent = fields.Float(string='Maverick %')
    alert = fields.Boolean(string='Alert')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.spend.analysis'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
