# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightCost(models.Model):
    _name = 'sf.freight.cost'
    _description = 'Freight Cost'
    _rec_name = 'carrier_id'
    _order = 'date desc'

    picking_id = fields.Many2one('stock.picking', string='Picking',
                                 ondelete='cascade')
    carrier_id = fields.Many2one('sf.freight.carrier', string='Carrier',
                                 required=True)
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.today)
    weight = fields.Float(string='Weight (kg)', default=0.0)
    volume = fields.Float(string='Volume (m3)', default=0.0)
    value = fields.Float(string='Goods Value', default=0.0)
    method = fields.Selection(related='carrier_id.cost_method',
                              string='Cost Method', readonly=True)
    unit_cost = fields.Float(string='Unit Cost', compute='_compute_unit_cost',
                             store=True)
    total_cost = fields.Float(string='Total Cost', compute='_compute_unit_cost',
                              store=True)
    state = fields.Selection([
        ('estimated', 'Estimated'),
        ('actual', 'Actual'),
    ], string='Status', default='estimated')

    @api.depends('weight', 'volume', 'value', 'carrier_id')
    def _compute_unit_cost(self):
        for cost in self:
            if not cost.carrier_id:
                cost.unit_cost = 0.0
                cost.total_cost = 0.0
                continue
            total = self.env['sf.freight.carrier'].compute_cost(
                cost.carrier_id, cost.weight, cost.volume, cost.value)
            cost.unit_cost = total
            cost.total_cost = total

    def action_mark_actual(self):
        for cost in self:
            cost.state = 'actual'