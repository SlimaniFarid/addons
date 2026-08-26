from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SpaAnamnesis(models.Model):
    _name = 'sf.spa.anamnesis'
    _description = 'Wellness Anamnesis'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread']
    _order = 'date desc'
    _sequence_code = 'sf.spa.anamnesis'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    therapist_id = fields.Many2one('sf.spa.therapist', string='Therapist', tracking=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    health_conditions = fields.Text(string='Health Conditions')
    allergies = fields.Text(string='Allergies')
    medications = fields.Text(string='Medications')
    preferences = fields.Text(string='Preferences (pressure, oils, music, temperature)')
    goals = fields.Selection([
        ('relaxation', 'Relaxation'),
        ('recovery', 'Sports Recovery'),
        ('slimming', 'Slimming'),
        ('anti_aging', 'Anti-Aging'),
        ('medical_support', 'Medical Support'),
        ('other', 'Other'),
    ], string='Goals', required=True)
    goal_details = fields.Text(string='Goal Details')
    contraindications = fields.Text(string='Contraindications')
    consent_data = fields.Boolean(string='Data Consent (GDPR)', default=True, required=True)
    client_plan_ids = fields.One2many('sf.spa.client.plan', 'anamnesis_id', string='Client Plans')

    @api.constrains('consent_data')
    def _check_consent(self):
        for record in self:
            if not record.consent_data:
                raise ValidationError(_('GDPR consent is required for anamnesis.'))

    def name_get(self):
        result = []
        for record in self:
            name = f'{record.name} - {record.partner_id.name}'
            result.append((record.id, name))
        return result