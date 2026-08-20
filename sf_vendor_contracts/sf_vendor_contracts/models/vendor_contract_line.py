# -*- coding: utf-8 -*-
from odoo import api, fields, models


class VendorContractLine(models.Model):
    _name = 'sf.vendor.contract.line'
    _description = 'Contract Line'
    _order = 'contract_id, id'

    contract_id = fields.Many2one('sf.vendor.contract',
                                  string='Contract', required=True,
                                  ondelete='cascade')
    product_id = fields.Many2one('product.product',
                                 string='Product')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price', default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self:
                                  self.env.company.currency_id)
    amount = fields.Monetary(string='Amount',
                             compute='_compute_amount', store=True)

    @api.depends('quantity', 'unit_price', 'currency_id')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price