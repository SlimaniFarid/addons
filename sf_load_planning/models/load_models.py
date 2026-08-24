# -*- coding: utf-8 -*-
"""Load planning models."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLoadPlan(models.Model):
    _name = 'sf.load.plan'
    _description = 'Load Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'departure_date desc'

    name = fields.Char(string='Load Reference', required=True, copy=False,
                       readonly=True, default='New')
    carrier_id = fields.Many2one('res.partner', string='Carrier')
    vehicle_ref = fields.Char(string='Vehicle / Trailer Ref')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    departure_date = fields.Datetime(string='Departure', required=True,
                                     default=fields.Datetime.now)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    stop_ids = fields.One2many('sf.load.stop', 'load_id', string='Route Stops',
                               copy=True)
    line_ids = fields.One2many('sf.load.line', 'load_id', string='Pickings')
    max_weight_kg = fields.Float(string='Max Weight (kg)')
    max_volume_m3 = fields.Float(string='Max Volume (m3)')
    max_pallets = fields.Integer(string='Max Pallets')
    total_weight_kg = fields.Float(string='Loaded Weight (kg)',
                                   compute='_compute_totals')
    total_volume_m3 = fields.Float(string='Loaded Volume (m3)',
                                   compute='_compute_totals')
    total_pallets = fields.Integer(string='Pallets',
                                   compute='_compute_totals')
    weight_over = fields.Boolean(compute='_compute_totals')
    volume_over = fields.Boolean(compute='_compute_totals')
    pallets_over = fields.Boolean(compute='_compute_totals')
    picking_count = fields.Integer(compute='_compute_totals')
    state = fields.Selection([
        ('draft', 'Draft'), ('planned', 'Planned'),
        ('loaded', 'Loaded'), ('departed', 'Departed'),
        ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.load.plan') or 'LOAD-NEW'
        return super().create(vals_list)

    def _compute_totals(self):
        for load in self:
            pickings = load.line_ids.mapped('picking_id')
            weight = 0.0
            volume = 0.0
            pallets = 0
            for picking in pickings:
                for move in picking.move_ids:
                    qty = move.product_uom_qty
                    weight += move.product_id.weight * qty
                    volume += (move.product_id.volume or 0.0) * qty
                pallets += picking.pallet_count or 1
            load.total_weight_kg = weight
            load.total_volume_m3 = volume
            load.total_pallets = pallets
            load.picking_count = len(pickings)
            load.weight_over = bool(load.max_weight_kg
                                    and weight > load.max_weight_kg)
            load.volume_over = bool(load.max_volume_m3
                                    and volume > load.max_volume_m3)
            load.pallets_over = bool(load.max_pallets
                                     and pallets > load.max_pallets)

    def action_plan(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Assign at least one picking.'))
        if self.weight_over or self.volume_over or self.pallets_over:
            raise UserError(_(
                'Capacity exceeded (weight/volume/pallets). Fix the load '
                'before planning.'))
        self.write({'state': 'planned'})

    def action_loaded(self):
        self.write({'state': 'loaded'})

    def action_depart(self):
        self.write({'state': 'departed'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class SfLoadLine(models.Model):
    _name = 'sf.load.line'
    _description = 'Load Line (Picking)'

    load_id = fields.Many2one('sf.load.plan', string='Load', required=True,
                              ondelete='cascade')
    picking_id = fields.Many2one('stock.picking', string='Delivery',
                                 required=True,
                                 domain=[('picking_type_id.code', '=',
                                          'outgoing')])
    partner_id = fields.Many2one(related='picking_id.partner_id')
    stop_id = fields.Many2one('sf.load.stop', string='Route Stop')
    pallet_count = fields.Integer(related='picking_id.pallet_count',
                                  string='Pallets')
    company_id = fields.Many2one(related='load_id.company_id', store=True)


class SfLoadStop(models.Model):
    _name = 'sf.load.stop'
    _description = 'Load Route Stop'
    _order = 'sequence, id'

    load_id = fields.Many2one('sf.load.plan', string='Load', required=True,
                              ondelete='cascade')
    sequence = fields.Integer(default=10)
    partner_id = fields.Many2one('res.partner', string='Stop / Customer',
                                 required=True)
    planned_arrival = fields.Datetime(string='Planned Arrival')
    notes = fields.Char(string='Notes')
    company_id = fields.Many2one(related='load_id.company_id', store=True)
