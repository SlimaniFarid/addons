# -*- coding: utf-8 -*-
from odoo import fields, models, _


class CpqConfigurator(models.Model):
    _name = 'sf.cpq.configurator'
    _description = 'CPQ Configurator'
    _rec_name = 'product_id'
    _order = 'product_id'

    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    attribute_ids = fields.Many2many('sf.cpq.attribute',
                                     string='Attributes')
    configuration_ids = fields.One2many('sf.cpq.configuration',
                                        'configurator_id',
                                        string='Configurations')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('product_uniq', 'unique(product_id)',
         'A configurator already exists for this product.'),
    ]