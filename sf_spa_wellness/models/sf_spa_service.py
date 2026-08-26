from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaService(models.Model):
    _name = 'sf.spa.service'
    _description = 'Spa Service'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sequence_code = 'sf.spa.service'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    category = fields.Selection([
        ('massage', 'Massage'),
        ('body_treatment', 'Body Treatment'),
        ('facial', 'Facial'),
        ('hydrotherapy', 'Hydrotherapy'),
        ('kinesiotherapy', 'Kinesiotherapy'),
        ('wellness', 'Wellness'),
        ('package', 'Package'),
        ('cure', 'Cure'),
    ], string='Category', required=True, tracking=True)
    duration_minutes = fields.Integer(string='Duration (Minutes)', required=True, default=60)
    resource_type_required = fields.Many2one(
        'sf.spa.resource',
        string='Required Resource Type',
        domain="[('resource_type', '!=', 'equipment')]",
        tracking=True
    )
    equipment_ids = fields.Many2many(
        'sf.spa.equipment',
        'sf_spa_service_equipment_rel',
        'service_id',
        'equipment_id',
        string='Required Equipment'
    )
    therapist_skill_ids = fields.Many2many(
        'sf.spa.skill',
        'sf_spa_service_skill_rel',
        'service_id',
        'skill_id',
        string='Required Skills'
    )
    price = fields.Monetary(string='Price', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    commission_rate = fields.Float(string='Commission Rate (%)', help='Override therapist default commission rate for this service')
    is_package = fields.Boolean(string='Is Package', default=False)
    is_cure = fields.Boolean(string='Is Cure', default=False)
    package_session_ids = fields.One2many('sf.spa.package.session', 'package_id', string='Package Sessions')
    cure_template_id = fields.Many2one('sf.spa.cure.template', string='Cure Template')
    active = fields.Boolean(default=True)
    booking_ids = fields.One2many('sf.spa.booking', 'service_id', string='Bookings')

    @api.constrains('duration_minutes')
    def _check_duration(self):
        for record in self:
            if record.duration_minutes <= 0:
                raise ValidationError(_('Duration must be positive.'))

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError(_('Price cannot be negative.'))

    @api.constrains('is_package', 'is_cure')
    def _check_package_cure(self):
        for record in self:
            if record.is_package and record.is_cure:
                raise ValidationError(_('A service cannot be both a package and a cure.'))

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.category:
                name = f'[{record.category}] {name}'
            result.append((record.id, name))
        return result