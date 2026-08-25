# -*- coding: utf-8 -*-
"""Return-to-vendor orders."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRtvOrder(models.Model):
    _name = 'sf.rtv.order'
    _description = 'Return to Vendor Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='RTV Number', required=True, copy=False,
                       readonly=True, default='New')
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True,
                                domain=[('supplier_rank', '>', 0)],
                                tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    origin_picking_id = fields.Many2one('stock.picking',
                                        string='Origin Receipt')
    reason = fields.Selection([
        ('defective', 'Defective / Quality'),
        ('wrong_item', 'Wrong Item Shipped'),
        ('overstock', 'Overstock Return'),
        ('recall', 'Supplier Recall'),
        ('warranty', 'Warranty Claim'),
        ('other', 'Other')], required=True, default='defective')
    description = fields.Text(string='Description / Defect Details')
    requested_date = fields.Date(string='Requested Date',
                                 default=fields.Date.today)
    authorization_ref = fields.Char(string='Vendor Authorization (RMA #)')
    line_ids = fields.One2many('sf.rtv.line', 'order_id', string='RTV Lines',
                               copy=True)
    total_value = fields.Float(string='Total RTV Value',
                               compute='_compute_total', store=True)
    return_picking_id = fields.Many2one('stock.picking',
                                        string='Return Picking',
                                        readonly=True, copy=False)
    debit_note_ref = fields.Char(string='Debit Note Ref')
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped to Vendor'), ('settled', 'Settled'),
        ('closed', 'Closed'), ('cancelled', 'Cancelled')],
        default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.rtv.order') or 'RTV-NEW'
        return super().create(vals_list)

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total_value = sum(rec.line_ids.mapped('subtotal'))

    def action_confirm(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Add at least one RTV line.'))
        self.write({'state': 'confirmed'})

    def action_create_return_picking(self):
        """Create an outgoing picking to the vendor."""
        self.ensure_one()
        if self.return_picking_id:
            raise UserError(_('Return picking already created.'))
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'outgoing'),
            ('company_id', '=', self.company_id.id)], limit=1)
        if not picking_type:
            raise UserError(_('No delivery picking type found.'))
        move_vals = []
        for line in self.line_ids.filtered(
                lambda l: l.disposition in ('return_credit',
                                            'return_repair')):
            move_vals.append((0, 0, {
                'name': _('RTV %s') % self.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_uom_id.id,
                'location_id': line.location_id.id
                or picking_type.default_location_src_id.id,
                'location_dest_id': self.env.ref(
                    'stock.stock_location_customers').id,
                'move_line_ids': [(0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom_id': line.product_uom_id.id,
                    'lot_id': line.lot_id.id,
                    'location_id': line.location_id.id
                    or picking_type.default_location_src_id.id,
                    'location_dest_id': self.env.ref(
                        'stock.stock_location_customers').id,
                })] if line.lot_id else [],
            }))
        if not move_vals:
            raise UserError(
                _('No lines with a return disposition to ship.'))
        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'partner_id': self.vendor_id.id,
            'origin': self.name,
            'location_id': picking_type.default_location_src_id.id,
            'move_ids': move_vals,
        })
        self.write({'return_picking_id': picking.id, 'state': 'shipped'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'view_mode': 'form',
        }

    def action_settle(self):
        self.ensure_one()
        if self.state != 'shipped':
            raise UserError(_('Ship the goods before settling.'))
        if not self.debit_note_ref:
            raise UserError(_('Enter the debit note reference.'))
        self.write({'state': 'settled'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_cancel(self):
        if self.return_picking_id and \
                self.return_picking_id.state == 'done':
            raise UserError(_('Return already shipped; cannot cancel.'))
        self.write({'state': 'cancelled'})


class SfRtvLine(models.Model):
    _name = 'sf.rtv.line'
    _description = 'RTV Line'
    _order = 'order_id, sequence, id'

    order_id = fields.Many2one('sf.rtv.order', string='RTV Order',
                               required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    product_uom_id = fields.Many2one(related='product_id.uom_id')
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial')
    location_id = fields.Many2one('stock.location', string='Stock Location')
    quantity = fields.Float(string='Qty', required=True, default=1.0)
    unit_cost = fields.Float(string='Unit Cost')
    subtotal = fields.Float(string='Value', compute='_compute_subtotal',
                            store=True)
    disposition = fields.Selection([
        ('return_credit', 'Return for Credit'),
        ('return_repair', 'Return for Repair'),
        ('replace', 'Vendor Replacement'),
        ('scrap', 'Scrap On Site')],
        required=True, default='return_credit')
    notes = fields.Char(string='Notes')
    company_id = fields.Many2one(related='order_id.company_id', store=True)
    currency_id = fields.Many2one(related='order_id.currency_id')

    @api.depends('quantity', 'unit_cost')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_cost

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.rtv.order'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

