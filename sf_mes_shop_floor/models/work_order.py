# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MesWorkOrder(models.Model):
    _name = 'sf.mes.work.order'
    _description = 'MES Work Order'
    _rec_name = 'name'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    mo_id = fields.Many2one('mrp.production', string='Manufacturing Order')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    station_id = fields.Many2one('sf.mes.station', string='Station',
                                 required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('done', 'Done'),
    ], string='Status', default='pending', tracking=True)
    operator_id = fields.Many2one('res.users', string='Operator')
    started_at = fields.Datetime(string='Started At')
    finished_at = fields.Datetime(string='Finished At')
    units_produced = fields.Float(string='Units Produced', default=0.0)
    quality_check_ids = fields.One2many('sf.mes.quality.check',
                                        'work_order_id',
                                        string='Quality Checks')
    downtime_ids = fields.One2many('sf.mes.downtime', 'work_order_id',
                                   string='Downtime Logs')
    duration_minutes = fields.Integer(string='Duration (min)',
                                      compute='_compute_duration')

    @api.depends('started_at', 'finished_at')
    def _compute_duration(self):
        for order in self:
            if order.started_at and order.finished_at:
                delta = order.finished_at - order.started_at
                order.duration_minutes = int(delta.total_seconds() // 60)
            else:
                order.duration_minutes = 0

    def action_start(self):
        for order in self:
            order.state = 'running'
            order.started_at = fields.Datetime.now()

    def action_pause(self):
        for order in self:
            order.state = 'paused'

    def action_resume(self):
        for order in self:
            order.state = 'running'

    def action_done(self):
        for order in self:
            order.state = 'done'
            order.finished_at = fields.Datetime.now()
            if not order.units_produced:
                order.units_produced = order.quantity

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.mes.downtime'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

