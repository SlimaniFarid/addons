# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    digital_delivery_ids = fields.One2many('sf.digital.delivery', 'order_id',
                                           string='Digital Deliveries')

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.state == 'sale':
                self.env['sf.digital.delivery']._create_from_order(order)
        return res