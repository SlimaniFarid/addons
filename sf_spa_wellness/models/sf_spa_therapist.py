from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaTherapist(models.Model):
    _name = 'sf.spa.therapist'
    _description = 'Spa Therapist'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sequence_code = 'sf.spa.therapist'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    skill_ids = fields.Many2many(
        'sf.spa.skill',
        'sf_spa_therapist_skill_rel',
        'therapist_id',
        'skill_id',
        string='Skills',
        tracking=True
    )
    certification_ids = fields.One2many('sf.spa.certification', 'therapist_id', string='Certifications')
    schedule_ids = fields.One2many('sf.spa.therapist.schedule', 'therapist_id', string='Weekly Schedule')
    commission_rate = fields.Float(string='Commission Rate (%)', default=0.0, tracking=True)
    commission_on_retail = fields.Float(string='Retail Commission (%)', default=0.0, tracking=True)
    active = fields.Boolean(default=True)
    booking_ids = fields.One2many('sf.spa.booking', 'therapist_id', string='Bookings')

    @api.constrains('commission_rate', 'commission_on_retail')
    def _check_commission_rates(self):
        for record in self:
            if record.commission_rate < 0 or record.commission_rate > 100:
                raise ValidationError(_('Commission rate must be between 0 and 100.'))
            if record.commission_on_retail < 0 or record.commission_on_retail > 100:
                raise ValidationError(_('Retail commission rate must be between 0 and 100.'))

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.partner_id:
                name = f'{record.partner_id.name} ({name})'
            result.append((record.id, name))
        return result

    def get_available_slots(self, date, resource_ids=None):
        self.ensure_one()
        day_of_week = date.weekday()
        schedules = self.schedule_ids.filtered(lambda s: s.day_of_week == str(day_of_week))
        if not schedules:
            return []
        slots = []
        for schedule in schedules:
            if resource_ids and schedule.resource_ids:
                if not any(r.id in resource_ids for r in schedule.resource_ids):
                    continue
            slots.append({
                'start': schedule.start_time,
                'end': schedule.end_time,
                'resources': schedule.resource_ids.ids if schedule.resource_ids else [],
            })
        return slots