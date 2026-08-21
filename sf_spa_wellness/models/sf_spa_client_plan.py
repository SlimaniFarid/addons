from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SpaClientPlan(models.Model):
    _name = 'sf.spa.client.plan'
    _description = 'Client Wellness Plan'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'
    _sequence_code = 'sf.spa.client.plan'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    anamnesis_id = fields.Many2one('sf.spa.anamnesis', string='Anamnesis')
    therapist_id = fields.Many2one('sf.spa.therapist', string='Therapist', tracking=True)
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    objective = fields.Char(string='Objective', required=True)
    recommended_service_ids = fields.Many2many(
        'sf.spa.service',
        'sf_spa_client_plan_service_rel',
        'plan_id',
        'service_id',
        string='Recommended Services'
    )
    recommended_frequency = fields.Selection([
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ], string='Recommended Frequency', default='monthly')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('reevaluated', 'Re-evaluated'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ], string='State', default='draft', tracking=True)
    nps_score = fields.Integer(string='NPS Score (0-10)', help='Net Promoter Score')
    nps_comment = fields.Text(string='NPS Comment')
    last_reevaluation = fields.Date(string='Last Re-evaluation')
    next_reevaluation = fields.Date(string='Next Re-evaluation', compute='_compute_next_reevaluation', store=True)
    booking_ids = fields.One2many('sf.spa.booking', 'client_plan_id', string='Bookings')

    @api.depends('last_reevaluation', 'recommended_frequency')
    def _compute_next_reevaluation(self):
        for record in self:
            if not record.last_reevaluation:
                record.next_reevaluation = False
                continue
            if record.recommended_frequency == 'weekly':
                record.next_reevaluation = record.last_reevaluation + relativedelta(weeks=1)
            elif record.recommended_frequency == 'biweekly':
                record.next_reevaluation = record.last_reevaluation + relativedelta(weeks=2)
            elif record.recommended_frequency == 'monthly':
                record.next_reevaluation = record.last_reevaluation + relativedelta(months=1)
            else:
                record.next_reevaluation = record.last_reevaluation + relativedelta(months=3)

    def action_activate(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'active'
                record.last_reevaluation = fields.Date.today()

    def action_reevaluate(self):
        for record in self:
            if record.state not in ('active', 'reevaluated'):
                continue
            record.state = 'reevaluated'
            record.last_reevaluation = fields.Date.today()

    def action_complete(self):
        for record in self:
            if record.state not in ('active', 'reevaluated'):
                continue
            record.state = 'completed'

    def action_archive(self):
        for record in self:
            record.state = 'archived'

    @api.constrains('nps_score')
    def _check_nps(self):
        for record in self:
            if record.nps_score is not None and (record.nps_score < 0 or record.nps_score > 10):
                raise ValidationError(_('NPS score must be between 0 and 10.'))