# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class SafetyStockProductRule(models.Model):
    _name = 'sf.safety.stock.rule'
    _description = 'Safety Stock Rule'
    _rec_name = 'product_id'
    _order = 'product_id'

    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
                                   required=True)
    service_level = fields.Selection([
        ('90', '90% (standard)'),
        ('95', '95% (high)'),
        ('99', '99% (critical)'),
    ], string='Service Level', default='95', required=True)
    demand_days = fields.Integer(string='Demand Window (days)', default=30,
                                 help="Number of past days used to compute "
                                      "average demand.")
    lead_time_days = fields.Integer(string='Lead Time (days)', default=7)
    safety_stock = fields.Float(string='Safety Stock',
                                compute='_compute_levels', store=True)
    reorder_point = fields.Float(string='Reorder Point',
                                 compute='_compute_levels', store=True)
    suggested_qty = fields.Float(string='Suggested Order Qty',
                                 compute='_compute_levels', store=True)
    current_stock = fields.Float(
        string='Current Stock',
        compute='_compute_current_stock',
        help="Quantity on hand in the rule's warehouse.")
    below_point = fields.Boolean(string='Below Reorder Point',
                                 compute='_compute_below_point')
    active = fields.Boolean(string='Active', default=True)
    demand_ids = fields.One2many('sf.safety.stock.demand', 'rule_id',
                                 string='Demand History')

    @api.depends('product_id')
    def _compute_current_stock(self):
        for rule in self:
            product = rule.product_id
            warehouse = rule.warehouse_id
            location = warehouse.lot_stock_id if warehouse else False
            if product and location:
                rule.current_stock = product.with_context(
                    location=location.id).qty_available
            else:
                rule.current_stock = 0.0

    @api.depends('demand_days', 'lead_time_days', 'service_level',
                 'demand_ids.quantity')
    def _compute_levels(self):
        for rule in self:
            rule._refresh_demand_history()
            total = sum(rule.demand_ids.mapped('quantity') or [0.0])
            days = max(rule.demand_days or 1, 1)
            avg_daily = total / days
            lead = max(rule.lead_time_days or 0, 0)
            z = {'90': 1.28, '95': 1.65, '99': 2.33}.get(
                rule.service_level, 1.65)
            safety = round(avg_daily * z * (lead ** 0.5), 2)
            rule.safety_stock = safety
            rule.reorder_point = round(avg_daily * lead + safety, 2)
            rule.suggested_qty = round(avg_daily * lead + safety
                                       - rule.current_stock, 2)

    @api.depends('current_stock', 'reorder_point')
    def _compute_below_point(self):
        for rule in self:
            rule.below_point = rule.current_stock < rule.reorder_point

    def _refresh_demand_history(self):
        """Recompute daily demand from outgoing stock moves."""
        for rule in self:
            if not rule.product_id or not rule.warehouse_id:
                continue
            start = fields.Date.today() - fields.timedelta(
                days=max(rule.demand_days or 1, 1))
            moves = self.env['stock.move'].search([
                ('product_id', '=', rule.product_id.id),
                ('location_dest_id.usage', '=', 'customer'),
                ('state', '=', 'done'),
                ('date', '>=', start),
            ])
            by_day = {}
            for move in moves:
                day = move.date.date()
                by_day[day] = by_day.get(day, 0.0) + move.product_qty
            lines = [{
                'rule_id': rule.id,
                'day': day,
                'quantity': qty,
            } for day, qty in sorted(by_day.items())]
            if rule.demand_ids:
                rule.demand_ids.unlink()
            if lines:
                self.env['sf.safety.stock.demand'].create(lines)


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'sf.safety.stock.demand'

    def action_refresh_business(self):
        """Pull on-hand qty and 30-day outbound usage for linked product."""
        for rec in self:
            product = getattr(rec, 'product_id', False)
            if not product:
                continue
            on_hand = product.qty_available
            frm = fields.Date.context_today(rec) - relativedelta(days=30)
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('location_dest_id.usage', '=', 'customer'),
                ('date', '>=', frm)])
            usage = sum(m.product_uom.qty for m in moves)
            rec.message_post(body=_(
                'On hand: {h:.2f}; 30-day outbound: {u:.2f} '
                '({m} move(s)).').format(h=on_hand, u=usage, m=len(moves)))
        return True
