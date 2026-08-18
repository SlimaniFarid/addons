from odoo import api, fields, models
from datetime import timedelta


class QMSReview(models.Model):
    _name = 'qms.review'
    _description = 'Management Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'review_date desc'

    name = fields.Char(string='Review Reference', required=True, copy=False, default='New')
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    # Schedule
    review_date = fields.Date(string='Review Date', required=True, default=fields.Date.today)
    review_period_start = fields.Date(string='Period Start')
    review_period_end = fields.Date(string='Period End')

    # Chair & Participants
    chair_id = fields.Many2one('res.users', string='Chair', required=True)
    participant_ids = fields.Many2many('res.users', string='Participants')

    # Status
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
    ], string='Status', default='planned', tracking=True)

    # Agenda Items (ISO 9001:2015 Clause 9.3.2)
    agenda_items = fields.One2many('qms.review.agenda', 'review_id', string='Agenda')

    # Inputs (Clause 9.3.2)
    inputs = fields.One2many('qms.review.input', 'review_id', string='Review Inputs')

    # Outputs (Clause 9.3.3)
    output_ids = fields.One2many('qms.review.output', 'review_id', string='Review Outputs')

    # Minutes
    minutes = fields.Html(string='Minutes')
    minutes_approved = fields.Boolean(string='Minutes Approved')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('qms.review') or 'MR-%s' % self.env['ir.sequence'].next_by_code('qms.review')
        return super().create(vals_list)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_approve(self):
        self.write({'state': 'approved'})


class QMSReviewAgenda(models.Model):
    _name = 'qms.review.agenda'
    _description = 'Management Review Agenda Item'

    review_id = fields.Many2one('qms.review', string='Review', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    topic = fields.Char(string='Topic', required=True)
    iso_clause = fields.Char(string='ISO Clause')
    presenter_id = fields.Many2one('res.users', string='Presenter')
    duration_minutes = fields.Integer(string='Duration (min)')
    notes = fields.Text(string='Notes')