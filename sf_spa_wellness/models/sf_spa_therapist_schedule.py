from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaTherapistSchedule(models.Model):
    _name = 'sf.spa.therapist.schedule'
    _description = 'Therapist Weekly Schedule'
    _inherit = ['sf.spa.company.mixin']
    _order = 'day_of_week, start_time'

    therapist_id = fields.Many2one('sf.spa.therapist', string='Therapist', required=True, ondelete='cascade')
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Day of Week', required=True)
    start_time = fields.Float(string='Start Time', required=True, help='Start time in hours (e.g., 9.0 for 9:00, 14.5 for 14:30)')
    end_time = fields.Float(string='End Time', required=True, help='End time in hours')
    resource_ids = fields.Many2many(
        'sf.spa.resource',
        'sf_spa_therapist_schedule_resource_rel',
        'schedule_id',
        'resource_id',
        string='Preferred Resources'
    )

    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        for record in self:
            if record.start_time < 0 or record.start_time >= 24:
                raise ValidationError(_('Start time must be between 0 and 24.'))
            if record.end_time < 0 or record.end_time > 24:
                raise ValidationError(_('End time must be between 0 and 24.'))
            if record.start_time >= record.end_time:
                raise ValidationError(_('Start time must be before end time.'))

    @api.constrains('therapist_id', 'day_of_week', 'start_time', 'end_time')
    def _check_overlap(self):
        for record in self:
            overlapping = self.search([
                ('therapist_id', '=', record.therapist_id.id),
                ('day_of_week', '=', record.day_of_week),
                ('id', '!=', record.id),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])
            if overlapping:
                raise ValidationError(_('Schedule overlaps with existing schedule for this therapist on this day.'))