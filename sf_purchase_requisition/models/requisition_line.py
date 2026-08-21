# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RequisitionLine(models.Model):
    _name = 'sf.purchase.requisition.requisition.line'
    _description = 'Requisition Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    requisition_id = fields.Many2one('sf_purchase_requisition.purchase.requisition.sf', string='Requisition Id')
    product_id = fields.Many2one('product.product', string='Product Id', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    price_estimated = fields.Monetary(string='Price Estimated', currency_field='currency_id')
    vendor_suggested = fields.Many2one('res.partner', string='Vendor Suggested')

