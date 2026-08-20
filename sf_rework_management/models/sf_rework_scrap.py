# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SfReworkScrap(models.Model):
    _name = 'sf.rework.scrap'
    _description = 'Rework Scrap'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.rework.management.activity.mixin']
    _order = 'id asc'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    order_id = fields.Many2one('sf.rework.order', string='Rework Order',
                               required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, ondelete='restrict')
    qty = fields.Float(string='Quantity', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    value = fields.Float(string='Value', compute='_compute_value', store=True)
    reason = fields.Text(string='Reason')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_qty_positive', 'CHECK (qty > 0)',
         'The scrap quantity must be greater than zero.'),
    ]

    @api.depends('product_id.uom_id')
    def _compute_name(self):
        for scrap in self:
            scrap.name = '%s / %s' % (scrap.order_id.name, scrap.product_id.name)

    @api.depends('product_id.standard_price', 'qty')
    def _compute_value(self):
        for scrap in self:
            scrap.value = scrap.qty * scrap.product_id.standard_price

    @api.constrains('qty')
    def _check_qty(self):
        for scrap in self:
            if scrap.qty <= 0:
                raise ValidationError(_('The scrap quantity must be greater than zero.'))

    @api.onchange('order_id', 'product_id')
    def _onchange_uom(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id