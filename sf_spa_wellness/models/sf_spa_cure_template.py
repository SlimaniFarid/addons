from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import json


class SpaCureTemplate(models.Model):
    _name = 'sf.spa.cure.template'
    _description = 'Cure Template'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread']
    _order = 'name'
    _sequence_code = 'sf.spa.cure.template'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    duration_days = fields.Integer(string='Duration (Days)', required=True, default=1)
    daily_sessions = fields.Json(string='Daily Sessions', default=lambda self: '[]',
        help='JSON structure: [{"day": 1, "sessions": [{"service_id": 1, "quantity": 1, "preferred_time": "10:00"}]}]')
    total_price = fields.Monetary(string='Total Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    description = fields.Html(string='Description')
    active = fields.Boolean(default=True)
    cure_instance_ids = fields.One2many('sf.spa.cure.instance', 'cure_template_id', string='Cure Instances')

    @api.constrains('duration_days')
    def _check_duration(self):
        for record in self:
            if record.duration_days <= 0:
                raise ValidationError(_('Duration must be positive.'))

    @api.constrains('daily_sessions')
    def _check_daily_sessions(self):
        for record in self:
            try:
                sessions = json.loads(record.daily_sessions) if isinstance(record.daily_sessions, str) else record.daily_sessions
                if not isinstance(sessions, list):
                    raise ValidationError(_('Daily sessions must be a JSON array.'))
                for day_data in sessions:
                    if not isinstance(day_data, dict):
                        raise ValidationError(_('Each day must be an object.'))
                    if 'day' not in day_data or 'sessions' not in day_data:
                        raise ValidationError(_('Each day must have "day" and "sessions" keys.'))
                    if not isinstance(day_data['sessions'], list):
                        raise ValidationError(_('Sessions must be an array.'))
                    for session in day_data['sessions']:
                        if not isinstance(session, dict) or 'service_id' not in session:
                            raise ValidationError(_('Each session must have a service_id.'))
            except json.JSONDecodeError:
                raise ValidationError(_('Invalid JSON format for daily sessions.'))

    def get_daily_schedule(self):
        self.ensure_one()
        sessions = json.loads(self.daily_sessions) if isinstance(self.daily_sessions, str) else self.daily_sessions
        return sessions