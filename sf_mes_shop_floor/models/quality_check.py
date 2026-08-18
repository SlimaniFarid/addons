# -*- coding: utf-8 -*-
from odoo import fields, models, _


class MesQualityCheck(models.Model):
    _name = 'sf.mes.quality.check'
    _description = 'MES Quality Check'
    _order = 'date desc'

    work_order_id = fields.Many2one('sf.mes.work.order', string='Work Order',
                                    ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    check_type = fields.Selection([
        ('dimensional', 'Dimensional'),
        ('visual', 'Visual'),
        ('functional', 'Functional'),
        ('other', 'Other'),
    ], string='Check Type', default='visual')
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    ], string='Result', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    note = fields.Text(string='Notes')