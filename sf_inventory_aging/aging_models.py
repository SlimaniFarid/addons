# -*- coding: utf-8 -*-
"""Inventory aging analysis."""
from odoo import api, fields, models, _


class SfAgingAnalysis(models.Model):
    _name = 'sf.aging.analysis'
    _description = 'Inventory Aging Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'as_of_date desc'

    name = fields.Char(string='Analysis', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    as_of_date = fields.Date(string='As Of', required=True,
                             default=fields.Date.today)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    b1_percent = fields.Float(string='Provision % 0-30d', default=0.0)
    b2_percent = fields.Float(string='Provision % 31-90d', default=5.0)
    b3_percent = fields.Float(string='Provision % 91-180d', default=15.0)
    b4_percent = fields.Float(string='Provision % 180+d', default=40.0)
    line_ids = fields.One2many('sf.aging.line', 'analysis_id',
                               string='Aging Lines')
    total_value = fields.Float(compute='_compute_totals')
    total_provision = fields.Float(compute='_compute_totals')
    dead_stock_count = fields.Integer(compute='_compute_totals')
    state = fields.Selection([('draft', 'Draft'), ('computed', 'Computed')],
                             default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.aging.analysis') or 'AGE-NEW'
        return super().create(vals_list)

    def _compute_totals(self):
        for rec in self:
            rec.total_value = sum(l.stock_value for l in rec.line_ids)
            rec.total_provision = sum(l.provision_amount for l in rec.line_ids)
            rec.dead_stock_count = len(rec.line_ids.filtered(
                lambda l: l.aging_bucket == 'b4'))

    def action_compute(self):
        self.ensure_one()
        self.line_ids.unlink()
        domain = [('company_id', '=', self.company_id.id),
                  ('quantity', '>', 0)]
        if self.warehouse_id:
            domain.append('location_id', 'in',
                          self.warehouse_id.lot_stock_id.child_ids.ids +
                          [self.warehouse_id.lot_stock_id.id])
        quants = self.env['stock.quant'].search(domain)
        MoveLine = self.env['stock.move.line']
        vals_list = []
        for quant in quants:
            last_move = MoveLine.search([
                ('product_id', '=', quant.product_id.id),
                ('state', '=', 'done'),
                ('location_id.usage', '=', 'internal')],
                order='date desc', limit=1)
            last_date = (fields.Date.to_date(last_move.date)
                         if last_move else self.as_of_date)
            days = (self.as_of_date - last_date).days
            if days <= 30:
                bucket, pct = 'b1', self.b1_percent
            elif days <= 90:
                bucket, pct = 'b2', self.b2_percent
            elif days <= 180:
                bucket, pct = 'b3', self.b3_percent
            else:
                bucket, pct = 'b4', self.b4_percent
            value = quant.quantity * (quant.product_id.standard_price or 0.0)
            vals_list.append({
                'analysis_id': self.id,
                'product_id': quant.product_id.id,
                'lot_id': quant.lot_id.id,
                'quantity': quant.quantity,
                'stock_value': value,
                'last_movement': last_date,
                'aging_days': days,
                'aging_bucket': bucket,
                'provision_percent': pct,
                'provision_amount': value * pct / 100.0,
            })
        if vals_list:
            self.env['sf.aging.line'].create(vals_list)
        self.write({'state': 'computed'})


class SfAgingLine(models.Model):
    _name = 'sf.aging.line'
    _description = 'Aging Line'

    analysis_id = fields.Many2one('sf.aging.analysis', required=True,
                                  ondelete='cascade')
    company_id = fields.Many2one(related='analysis_id.company_id', store=True)
    currency_id = fields.Many2one(related='analysis_id.currency_id')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial')
    quantity = fields.Float(string='Qty')
    stock_value = fields.Float(string='Stock Value')
    last_movement = fields.Date(string='Last Movement')
    aging_days = fields.Integer(string='Aging (days)')
    aging_bucket = fields.Selection([
        ('b1', '0-30 days'), ('b2', '31-90 days'),
        ('b3', '91-180 days'), ('b4', '180+ days')], string='Bucket')
    provision_percent = fields.Float(string='Provision %')
    provision_amount = fields.Float(string='Provision')
