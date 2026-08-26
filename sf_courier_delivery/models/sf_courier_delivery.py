# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfCourierDelivery(models.Model):
    _name = 'sf.courier.delivery'
    _description = 'Courier Delivery'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.courier.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    order_id = fields.Many2one('sf.courier.order', string='Request', required=True, ondelete='cascade')
    courier_id = fields.Many2one('res.partner', string='Courier', ondelete='restrict',
                                     domain="[('is_company', '=', False)]")
    route_id = fields.Many2one('sf.courier.route', string='Route', ondelete='set null')
    parcel_description = fields.Char(string='Parcel Description')
    weight_kg = fields.Float(string='Weight (kg)')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    delivery_date = fields.Datetime(string='Delivery Date')
    proof_type = fields.Selection([
        ('signature', 'Signature'),
        ('photo', 'Photo'),
        ('none', 'None'),
    ], string='Proof Type')
    proof_signature = fields.Binary(string='Signature Proof', attachment=True)
    proof_photo = fields.Binary(string='Photo Proof', attachment=True)
    failure_reason = fields.Selection([
        ('absent', 'Recipient Absent'),
        ('wrong_address', 'Wrong Address'),
        ('refused', 'Recipient Refused'),
        ('damaged', 'Parcel Damaged'),
        ('other', 'Other'),
    ], string='Failure Reason')
    return_date = fields.Datetime(string='Return Date')
    attempt_ids = fields.One2many('sf.courier.delivery.attempt', 'delivery_id', string='Attempts')
    price = fields.Monetary(string='Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.courier.delivery')
            if vals.get('price') is None:
                vals['price'] = float(self.env['ir.config_parameter'].sudo().get_param(
                    'sf_courier_delivery.default_price', '0.0'
                ))
            if not vals.get('company_id') and vals.get('order_id'):
                order = self.env['sf.courier.order'].browse(vals['order_id'])
                vals['company_id'] = order.company_id.id
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_courier_delivery.group_sf_courier_manager'):
            raise UserError(_('Only a courier manager can perform this action.'))

    def _check_proof(self):
        if not self.proof_type or (not self.proof_signature and not self.proof_photo):
            raise UserError(_('A delivery requires a proof (signature or photo).'))

    def write(self, vals):
        if any(d.state == 'delivered' for d in self) and any(
            f in vals for f in ('courier_id', 'route_id', 'parcel_description', 'weight_kg',
                                'price', 'state', 'proof_type', 'proof_signature',
                                'proof_photo', 'failure_reason', 'return_date')
        ):
            raise UserError(_('A delivered delivery cannot be modified.'))
        if 'price' in vals and not self.env.user.has_group('sf_courier_delivery.group_sf_courier_manager'):
            raise UserError(_('Only a courier manager can change the price.'))
        return super().write(vals)

    def action_assign(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft deliveries can be assigned.'))
        if not self.courier_id:
            raise UserError(_('Select a courier before assigning the delivery.'))
        self.state = 'assigned'

    def action_start(self):
        self.ensure_one()
        if self.state != 'assigned':
            raise UserError(_('Only assigned deliveries can be started.'))
        routes = self.env['sf.courier.route'].search([
            ('courier_id', '=', self.courier_id.id),
            ('date', '=', fields.Date.context_today(self)),
        ])
        if not routes:
            raise UserError(_('The courier has no route planned for today.'))
        self.state = 'in_transit'

    def action_deliver(self):
        self.ensure_one()
        if self.state != 'in_transit':
            raise UserError(_('Only in-transit deliveries can be marked delivered.'))
        self._check_proof()
        self.state = 'delivered'
        self.delivery_date = fields.Datetime.now()
        self.env['sf.courier.delivery.attempt'].create({
            'delivery_id': self.id,
            'result': 'delivered',
            'notes': 'Delivered with %s proof.' % (self.proof_type or 'none'),
        })
        return self.env.ref('sf_courier_delivery.action_report_delivery_ticket').report_action(self)

    def action_fail(self, reason='other'):
        self.ensure_one()
        if self.state not in ('in_transit', 'assigned'):
            raise UserError(_('Only in-transit or assigned deliveries can fail.'))
        if reason not in ('absent', 'wrong_address', 'refused', 'damaged', 'other'):
            raise UserError(_('Invalid failure reason.'))
        self.state = 'failed'
        self.failure_reason = reason
        self.env['sf.courier.delivery.attempt'].create({
            'delivery_id': self.id,
            'result': 'failed',
            'failure_reason': reason,
        })

    def action_retry(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'failed':
            raise UserError(_('Only failed deliveries can be retried.'))
        if self.failure_reason in ('refused', 'damaged'):
            raise UserError(_('This failure cannot be retried, return the parcel instead.'))
        self.state = 'in_transit'

    def action_return(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'failed':
            raise UserError(_('Only failed deliveries can be returned.'))
        self.state = 'returned'
        self.return_date = fields.Datetime.now()

    def action_cancel(self):
        self.ensure_one()
        if self.state in ('delivered', 'returned'):
            raise UserError(_('A %s delivery cannot be cancelled.') % self.state)
        self._check_manager()
        self.state = 'cancelled'