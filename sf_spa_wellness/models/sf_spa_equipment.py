from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaEquipment(models.Model):
    _name = 'sf.spa.equipment'
    _description = 'Spa Equipment'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sequence_code = 'sf.spa.equipment'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    equipment_type = fields.Selection([
        ('table', 'Table'),
        ('stones', 'Stones'),
        ('towels', 'Towels'),
        ('oils', 'Oils'),
        ('device', 'Device'),
        ('consumable', 'Consumable'),
        ('other', 'Other'),
    ], string='Equipment Type', required=True, tracking=True)
    quantity_total = fields.Integer(string='Total Quantity', default=1, required=True)
    quantity_available = fields.Integer(
        string='Available Quantity',
        compute='_compute_quantity_available',
        store=True
    )
    maintenance_date = fields.Date(string='Maintenance Date')
    resource_ids = fields.Many2many(
        'sf.spa.resource',
        'sf_spa_resource_equipment_rel',
        'equipment_id',
        'resource_id',
        string='Resources'
    )
    active = fields.Boolean(default=True)

    @api.depends('quantity_total')
    def _compute_quantity_available(self):
        for record in self:
            booked_qty = 0
            if record.resource_ids:
                bookings = self.env['sf.spa.booking'].search([
                    ('resource_id', 'in', record.resource_ids.ids),
                    ('state', 'in', ['confirmed', 'in_progress']),
                ])
                for booking in bookings:
                    if record in booking.resource_id.equipment_ids:
                        booked_qty += 1
            record.quantity_available = record.quantity_total - booked_qty

    @api.constrains('quantity_total')
    def _check_quantity_total(self):
        for record in self:
            if record.quantity_total < 0:
                raise ValidationError(_('Total quantity cannot be negative.'))

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.equipment_type:
                name = f'[{record.equipment_type}] {name}'
            result.append((record.id, name))
        return result