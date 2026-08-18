# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class WavePicking(models.Model):
    _name = 'sf.wave.picking'
    _description = 'Warehouse Wave'
    _rec_name = 'name'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('released', 'Released'),
        ('done', 'Done'),
    ], string='Status', default='draft', tracking=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    picking_type_id = fields.Many2one('stock.picking.type',
                                      string='Picking Type')
    picking_ids = fields.Many2many('stock.picking', string='Pickings')
    move_count = fields.Integer(string='Move Lines',
                                compute='_compute_counts')
    done_lines = fields.Integer(string='Done Lines',
                                compute='_compute_counts')
    progress = fields.Float(string='Progress %', compute='_compute_counts',
                            store=True)
    date_start = fields.Datetime(string='Release Date')
    note = fields.Text(string='Notes')

    @api.depends('picking_ids.move_ids.picked',
                 'picking_ids.move_ids.product_uom_qty')
    def _compute_counts(self):
        for wave in self:
            lines = wave.picking_ids.move_ids
            total = sum(lines.mapped('product_uom_qty'))
            done = sum(line.product_uom_qty for line in lines
                       if line.quantity_done)
            wave.move_count = len(lines)
            wave.done_lines = int(round(done))
            wave.progress = total and min(round(done / total * 100, 1),
                                          100.0) or 0.0

    def action_release(self):
        for wave in self:
            wave.picking_ids.write({'state': 'assigned'})
            wave.state = 'released'
            wave.date_start = fields.Datetime.now()

    def action_done(self):
        for wave in self:
            wave.picking_ids.button_validate()
            wave.state = 'done'

    @api.model
    def create_wave_from_pickings(self, picking_ids):
        """Create a wave containing the given picking records."""
        pickings = self.env['stock.picking'].browse(picking_ids)
        if not pickings:
            return self
        warehouse = pickings[:1].warehouse_id or pickings[:1].picking_type_id.warehouse_id
        ptype = pickings[:1].picking_type_id
        seq = self.env['ir.sequence'].next_by_code('sf.wave.picking') or 'WAVE-%04d' % (
            self.search_count([]) + 1)
        wave = self.create({
            'name': seq,
            'warehouse_id': warehouse.id or False,
            'picking_type_id': ptype.id or False,
            'picking_ids': [(6, 0, pickings.ids)],
        })
        pickings.write({'sf_wave_id': wave.id})
        return wave