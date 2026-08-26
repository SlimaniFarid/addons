# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfLaundryItem(models.Model):
    _name = 'sf.laundry.item'
    _description = 'Laundry Item'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.laundry.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    order_id = fields.Many2one('sf.laundry.order', string='Order', required=True, ondelete='cascade')
    item_type = fields.Many2one('sf.laundry.item.type', string='Item Type', ondelete='restrict')
    description = fields.Char(string='Description')
    service = fields.Selection([
        ('wash', 'Wash'),
        ('dry_clean', 'Dry Clean'),
        ('iron', 'Iron'),
        ('full_service', 'Full Service'),
    ], string='Service', required=True, default='wash')
    qty = fields.Integer(string='Quantity', required=True, default=1)
    price_unit = fields.Monetary(string='Unit Price', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, currency_field='currency_id')
    state = fields.Selection([
        ('received', 'Received'),
        ('in_progress', 'In Progress'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('lost', 'Lost'),
    ], string='Status', default='received', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('qty', 'price_unit')
    def _compute_subtotal(self):
        for item in self:
            item.subtotal = item.qty * item.price_unit

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.laundry.item')
            if vals.get('qty', 0) <= 0:
                raise UserError(_('Quantities must be strictly positive.'))
            if not vals.get('price_unit'):
                item_type = self.env['sf.laundry.item.type'].browse(vals.get('item_type')) if vals.get('item_type') else self.env['sf.laundry.item.type']
                vals['price_unit'] = item_type.price_unit or 0.0
            vals.setdefault('company_id', self.env.company.id)
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('qty') is not None and vals['qty'] <= 0:
            raise UserError(_('Quantities must be strictly positive.'))
        if self.order_id.state == 'delivered' and self:
            raise UserError(_('Items of a delivered order cannot be modified.'))
        return super().write(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_laundry.group_sf_laundry_manager'):
            raise UserError(_('Only a laundry manager can perform this action.'))

    def action_start(self):
        self.ensure_one()
        if self.state != 'received':
            raise UserError(_('Only received items can be started.'))
        self.state = 'in_progress'

    def action_ready(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress items can be marked ready.'))
        self.state = 'ready'

    def action_mark_lost(self):
        self.ensure_one()
        self._check_manager()
        self.state = 'lost'

    def action_regularize(self):
        self.ensure_one()
        self._check_manager()
        self.state = 'in_progress'