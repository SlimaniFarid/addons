# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class LotExt(models.Model):
    _inherit = 'stock.lot'

    quality_status = fields.Selection([
        ('ok', 'OK'),
        ('warning', 'Warning'),
        ('blocked', 'Blocked'),
    ], string='Quality Status', default='ok', tracking=True)
    batch_origin = fields.Char(string='Batch Origin')
    expiry_date = fields.Date(string='Expiry Date')
    recall_ids = fields.One2many('sf.traceability.recall', 'lot_id',
                                 string='Recalls')
    movement_history = fields.Text(string='Movement History',
                                   compute='_compute_movement_history')

    @api.depends('quality_status')
    def _check_blocked_lots(self):
        for lot in self:
            if lot.quality_status == 'blocked':
                lot.message_post(
                    body=_('Batch %s marked as blocked. Do not ship.') %
                    lot.name)

    @api.depends('id')
    def _compute_movement_history(self):
        for lot in self:
            lines = self.env['stock.move.line'].search([
                ('lot_id', '=', lot.id),
                ('state', '=', 'done'),
            ], order='date desc', limit=20)
            entries = []
            for line in lines:
                picking = line.move_id.picking_id
                partner = picking.partner_id.display_name if picking else ''
                entries.append(
                    '%s | %s -> %s | %s x %s | %s' % (
                        line.date.strftime('%Y-%m-%d'),
                        line.location_id.display_name,
                        line.location_dest_id.display_name,
                        line.product_id.name, line.quantity, partner))
            lot.movement_history = '\n'.join(entries)