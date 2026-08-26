# -*- coding: utf-8 -*-
"""Backorder allocation runs."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBoAllocation(models.Model):
    _name = 'sf.bo.allocation'
    _description = 'Backorder Allocation Run'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Run', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    available_qty = fields.Float(string='Available Stock',
                                 compute='_compute_available')
    weight_customer = fields.Float(string='Weight: Customer Priority',
                                   default=1.0)
    weight_value = fields.Float(string='Weight: Order Value', default=1.0)
    weight_lateness = fields.Float(string='Weight: Days Late', default=1.0)
    line_ids = fields.One2many('sf.bo.allocation.line', 'run_id',
                               string='Allocations')
    allocated_qty = fields.Float(compute='_compute_allocated')
    state = fields.Selection([('draft', 'Draft'), ('computed', 'Computed'),
                              ('applied', 'Applied')], default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.bo.allocation') or 'BOAL-NEW'
        return super().create(vals_list)

    def _compute_available(self):
        for rec in self:
            quants = sum(self.env['stock.quant'].search([
                ('product_id', '=', rec.product_id.id),
                ('location_id.usage', '=', 'internal')]).mapped(
                'available_quantity'))
            rec.available_qty = quants

    def _compute_allocated(self):
        for rec in self:
            rec.allocated_qty = sum(rec.line_ids.mapped('allocated_qty'))

    def action_compute(self):
        self.ensure_one()
        self.line_ids.unlink()
        pickings = self.env['stock.picking'].search([
            ('company_id', '=', self.company_id.id),
            ('state', 'in', ('confirmed', 'waiting', 'assigned')),
            ('picking_type_id.code', '=', 'outgoing'),
            ('move_ids.product_id', '=', self.product_id.id)])
        lines = []
        for picking in pickings:
            qty = sum(picking.move_ids.filtered(
                lambda m: m.product_id == self.product_id).mapped(
                'product_uom_qty'))
            done = sum(picking.move_ids.filtered(
                lambda m: m.product_id == self.product_id).mapped(
                'quantity'))
            shortage = max(qty - done, 0)
            if shortage <= 0:
                continue
            order = self.env['sale.order'].search(
                [('picking_ids', 'in', picking.id)], limit=1)
            commitment = order.commitment_date or picking.scheduled_date
            days_late = max((fields.Date.context_today(self) -
                             fields.Date.to_date(commitment)).days, 0)
            value = order.amount_total if order else 0.0
            score = (self.weight_lateness * days_late
                     + self.weight_value * min(value / 1000.0, 100)
                     + self.weight_customer * 10)
            lines.append({'run_id': self.id, 'picking_id': picking.id,
                          'partner_id': picking.partner_id.id,
                          'shortage_qty': shortage, 'days_late': days_late,
                          'order_value': value, 'priority_score': score})
        lines.sort(key=lambda l: -l['priority_score'])
        remaining = self.available_qty
        for line in lines:
            alloc = min(remaining, line['shortage_qty'])
            line['allocated_qty'] = alloc
            remaining -= alloc
        if lines:
            self.env['sf.bo.allocation.line'].create(lines)
        self.write({'state': 'computed'})

    def action_apply(self):
        self.ensure_one()
        if self.state != 'computed':
            raise UserError(_('Compute before applying.'))
        for line in self.line_ids:
            if line.allocated_qty > 0 and line.picking_id.state in (
                    'confirmed', 'waiting'):
                line.picking_id.action_assign()
        self.write({'state': 'applied'})


class SfBoAllocationLine(models.Model):
    _name = 'sf.bo.allocation.line'
    _description = 'Backorder Allocation Line'

    run_id = fields.Many2one('sf.bo.allocation', required=True,
                             ondelete='cascade')
    company_id = fields.Many2one(related='run_id.company_id', store=True)
    currency_id = fields.Many2one(related='run_id.company_id.currency_id')
    picking_id = fields.Many2one('stock.picking', string='Delivery',
                                 required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    shortage_qty = fields.Float(string='Shortage')
    days_late = fields.Integer(string='Days Late')
    order_value = fields.Float(string='Order Value')
    priority_score = fields.Float(string='Priority Score')
    allocated_qty = fields.Float(string='Allocated')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.bo.allocation'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.bo.allocation'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
