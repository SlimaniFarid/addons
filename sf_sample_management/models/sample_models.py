# -*- coding: utf-8 -*-
"""Sample request management."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class SfSampleRequest(models.Model):
    _name = 'sf.sample.request'
    _description = 'Sample Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer / Prospect',
                                 required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    requester_id = fields.Many2one('res.users', string='Requested By',
                                   default=lambda s: s.env.uid)
    purpose = fields.Selection([
        ('evaluation', 'Product Evaluation'),
        ('trade_show', 'Trade Show'),
        ('lab_test', 'Lab Test / Validation'),
        ('press', 'Press / Marketing'),
        ('other', 'Other')], required=True, default='evaluation')
    line_ids = fields.One2many('sf.sample.line', 'request_id',
                               string='Sample Lines', copy=True)
    total_cost = fields.Float(string='Total Cost',
                              compute='_compute_total_cost', store=True)
    shipping_cost = fields.Float(string='Shipping Cost')
    followup_date = fields.Date(string='Follow-up Date')
    shipment_ref = fields.Char(string='Shipment / Tracking Ref')
    picking_id = fields.Many2one('stock.picking', string='Delivery',
                                 readonly=True, copy=False)
    sale_order_id = fields.Many2one('sale.order', string='Converted Sale Order',
                                    readonly=True, copy=False)
    feedback_ids = fields.One2many('sf.sample.feedback', 'request_id',
                                   string='Feedback')
    outcome = fields.Selection([
        ('pending', 'Pending'), ('won', 'Won'), ('lost', 'Lost')],
        default='pending', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('approved', 'Approved'),
        ('shipped', 'Shipped'), ('feedback', 'Feedback Received'),
        ('converted', 'Converted'), ('closed', 'Closed'),
        ('cancelled', 'Cancelled')], default='draft', tracking=True,
        copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.sample.request') or 'SMP-NEW'
        return super().create(vals_list)

    @api.depends('line_ids.subtotal', 'shipping_cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = (sum(rec.line_ids.mapped('subtotal'))
                              + rec.shipping_cost)

    def action_approve(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Add at least one sample line.'))
        self.write({'state': 'approved'})

    def action_ship(self):
        self.ensure_one()
        if self.state != 'approved':
            raise UserError(_('Approve the request before shipping.'))
        if not self.shipment_ref:
            raise UserError(_('Enter the shipment / tracking reference.'))
        self.write({'state': 'shipped'})

    def action_receive_feedback(self):
        self.ensure_one()
        if not self.feedback_ids:
            raise UserError(_('Record at least one feedback line.'))
        self.write({'state': 'feedback'})

    def action_convert(self):
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(_('Link the resulting sale order first.'))
        self.write({'state': 'converted', 'outcome': 'won'})

    def action_mark_lost(self):
        self.write({'outcome': 'lost', 'state': 'closed'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class SfSampleLine(models.Model):
    _name = 'sf.sample.line'
    _description = 'Sample Line'

    request_id = fields.Many2one('sf.sample.request', required=True,
                                 ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    quantity = fields.Float(string='Qty', required=True, default=1.0)
    unit_cost = fields.Float(string='Unit Cost')
    subtotal = fields.Float(string='Cost', compute='_compute_subtotal',
                            store=True)
    notes = fields.Char(string='Notes')
    company_id = fields.Many2one(related='request_id.company_id', store=True)

    @api.depends('quantity', 'unit_cost')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_cost


class SfSampleFeedback(models.Model):
    _name = 'sf.sample.feedback'
    _description = 'Sample Feedback'

    request_id = fields.Many2one('sf.sample.request', required=True,
                                 ondelete='cascade')
    feedback_date = fields.Date(string='Date', default=fields.Date.today)
    contact_name = fields.Char(string='Contact')
    rating = fields.Selection([
        ('1', '1 - Poor'), ('2', '2'), ('3', '3 - Average'),
        ('4', '4'), ('5', '5 - Excellent')], string='Rating')
    comments = fields.Text(string='Comments')
    company_id = fields.Many2one(related='request_id.company_id', store=True)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.sample.request'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'sf.sample.request'

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
