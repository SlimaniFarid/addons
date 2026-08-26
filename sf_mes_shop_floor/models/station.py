# -*- coding: utf-8 -*-
from odoo import fields, models, _


class MesStation(models.Model):
    _name = 'sf.mes.station'
    _description = 'MES Station'
    _rec_name = 'name'
    _order = 'code'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Workcenter')
    location = fields.Char(string='Location')
    operator_id = fields.Many2one('res.users', string='Current Operator')
    work_order_ids = fields.One2many('sf.mes.work.order', 'station_id',
                                     string='Work Orders')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Station code must be unique.'),
    ]