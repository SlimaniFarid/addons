# -*- coding: utf-8 -*-
from odoo import fields, models, _


class SafetyStockDemand(models.Model):
    _name = 'sf.safety.stock.demand'
    _description = 'Safety Stock Daily Demand'
    _rec_name = 'day'
    _order = 'day desc'

    rule_id = fields.Many2one('sf.safety.stock.rule', string='Rule',
                              required=True, ondelete='cascade')
    day = fields.Date(string='Day', required=True)
    quantity = fields.Float(string='Quantity', required=True)

    _sql_constraints = [
        ('day_uniq', 'unique(rule_id, day)',
         'Only one demand entry per rule and day.'),
    ]