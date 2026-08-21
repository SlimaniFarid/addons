# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfYardZone(models.Model):
    _name = 'sf.yard.zone'
    _description = 'Yard Zone'
    _order = 'sequence, id'

    name = fields.Char(string='Zone Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(default=10)
    zone_type = fields.Selection([
        ('dock', 'Dock Doors'),
        ('parking', 'Trailer Parking'),
        ('waiting', 'Waiting Area'),
        ('maintenance', 'Maintenance'),
        ('customs', 'Customs Bonded'),
        ('cold', 'Cold Chain Staging'),
    ], string='Zone Type', required=True, default='parking')
    capacity = fields.Integer(string='Capacity (spots)',
                              compute='_compute_capacity', store=True)
    location_ids = fields.One2many('sf.yard.location', 'zone_id',
                                   string='Locations')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, store=True,
                                 default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('sf_yard_zone_code_uniq',
         'unique(code, company_id)',
         'Zone code must be unique per company.'),
    ]

    @api.depends('location_ids')
    def _compute_capacity(self):
        for zone in self:
            zone.capacity = len(zone.location_ids)


class SfYardLocation(models.Model):
    _name = 'sf.yard.location'
    _description = 'Yard Location'
    _order = 'zone_id, name'

    name = fields.Char(string='Spot Code', required=True,
                       help='e.g. A-01, DOCK-04')
    zone_id = fields.Many2one('sf.yard.zone', string='Zone',
                              required=True, ondelete='restrict', index=True)
    location_type = fields.Selection(related='zone_id.zone_type', store=True)
    x = fields.Integer(string='X')
    y = fields.Integer(string='Y')
    max_weight = fields.Float(string='Max Weight (kg)')
    trailer_id = fields.Many2one('sf.yard.trailer', string='Current Trailer',
                                 ondelete='set null', readonly=True,
                                 copy=False)
    occupied = fields.Boolean(string='Occupied', compute='_compute_occupied',
                              store=True)
    company_id = fields.Many2one(related='zone_id.company_id', store=True)

    _sql_constraints = [
        ('sf_yard_loc_name_uniq',
         'unique(name, company_id)',
         'Location code must be unique per company.'),
    ]

    @api.depends('trailer_id')
    def _compute_occupied(self):
        for loc in self:
            loc.occupied = bool(loc.trailer_id)

    @api.constrains('trailer_id')
    def _check_single_trailer(self):
        for loc in self:
            if loc.trailer_id and loc.trailer_id.current_location_id != loc:
                raise UserError(_(
                    'Location %s: trailer must point back to this '
                    'location.') % loc.name)

    def action_release(self):
        for loc in self:
            if loc.trailer_id:
                loc.trailer_id.write({
                    'current_location_id': False,
                    'status': 'at_yard',
                })
