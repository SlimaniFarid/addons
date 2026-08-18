# -*- coding: utf-8 -*-
from odoo import fields, models, _


class MesDowntime(models.Model):
    _name = 'sf.mes.downtime'
    _description = 'MES Downtime'
    _order = 'start desc'

    work_order_id = fields.Many2one('sf.mes.work.order', string='Work Order',
                                    ondelete='cascade')
    station_id = fields.Many2one('sf.mes.station', string='Station')
    start = fields.Datetime(string='Start', required=True,
                            default=fields.Datetime.now)
    end = fields.Datetime(string='End')
    reason = fields.Char(string='Reason')
    minutes = fields.Integer(string='Minutes', compute='_compute_minutes')

    def _compute_minutes(self):
        for dt in self:
            if dt.start and dt.end:
                delta = dt.end - dt.start
                dt.minutes = int(delta.total_seconds() // 60)
            else:
                dt.minutes = 0