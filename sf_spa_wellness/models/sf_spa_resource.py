from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SpaResource(models.Model):
    _name = 'sf.spa.resource'
    _description = 'Spa Resource'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sequence_code = 'sf.spa.resource'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    resource_type = fields.Selection([
        ('cabin', 'Cabin'),
        ('pool', 'Pool'),
        ('sauna', 'Sauna'),
        ('hammam', 'Hammam'),
        ('relaxation_room', 'Relaxation Room'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ], string='Resource Type', required=True, tracking=True)
    cabin_type = fields.Selection([
        ('solo', 'Solo'),
        ('duo', 'Duo'),
        ('vichy', 'Vichy Shower'),
        ('hydrojet', 'Hydrojet'),
        ('wet_table', 'Wet Table'),
        ('dry_table', 'Dry Table'),
        ('multi', 'Multi-purpose'),
    ], string='Cabin Type')
    capacity = fields.Integer(string='Capacity', default=1)
    equipment_ids = fields.Many2many(
        'sf.spa.equipment',
        'sf_spa_resource_equipment_rel',
        'resource_id',
        'equipment_id',
        string='Equipment'
    )
    location = fields.Char(string='Location')
    active = fields.Boolean(default=True)
    booking_ids = fields.One2many('sf.spa.booking', 'resource_id', string='Bookings')
    booking_count = fields.Integer(string='Booking Count', compute='_compute_booking_count')

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for record in self:
            record.booking_count = len(record.booking_ids.filtered(lambda b: b.state in ('confirmed', 'in_progress')))

    def action_view_bookings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bookings',
            'res_model': 'sf.spa.booking',
            'view_mode': 'list,form',
            'domain': [('resource_id', '=', self.id), ('state', 'in', ['confirmed', 'in_progress'])],
            'context': {'default_resource_id': self.id},
        }

    @api.constrains('resource_type', 'cabin_type')
    def _check_cabin_type(self):
        for record in self:
            if record.resource_type != 'cabin' and record.cabin_type:
                raise ValidationError(_('Cabin type can only be set for cabin resources.'))

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.resource_type:
                name = f'[{record.resource_type}] {name}'
            result.append((record.id, name))
        return result