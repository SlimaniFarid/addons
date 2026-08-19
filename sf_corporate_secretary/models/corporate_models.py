# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CorporateOrg(models.Model):
    _name = 'sf.corporate.org'
    _description = 'Corporate Organ'
    _order = 'name'

    name = fields.Char(string='Name', required=True, index=True)
    org_type = fields.Selection([
        ('aga', 'Annual General Meeting (AGA)'),
        ('age', 'Extraordinary General Meeting (AGE)'),
        ('ca', 'Board of Directors (CA)'),
        ('cs', 'Supervisory Board (CS)'),
        ('other', 'Other'),
    ], string='Organ type', default='aga', required=True)
    notice_days = fields.Integer(string='Notice period (days)')
    chairperson_id = fields.Many2one('res.partner', string='Chairperson',
                                     ondelete='restrict')
    members = fields.Many2many('res.partner', string='Members')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.corporate.org')
            vals['name'] = 'ORG-%s' % seq
        return super().create(vals)


class CorporateMeeting(models.Model):
    _name = 'sf.corporate.meeting'
    _description = 'Corporate Meeting'
    _order = 'scheduled_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    org_id = fields.Many2one('sf.corporate.org', string='Organ',
                             required=True, ondelete='restrict', index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    scheduled_date = fields.Date(string='Scheduled date', required=True)
    location = fields.Char(string='Location')
    notice_date = fields.Date(string='Notice date', readonly=True,
                              compute='_compute_notice_date', store=True)
    notice_sent = fields.Boolean(string='Notice sent', default=False)
    minutes = fields.Html(string='Minutes (PV)')
    minutes_done_date = fields.Date(string='Minutes done date', readonly=True)
    recorded_by = fields.Many2one('res.users', string='Recorded by',
                                  readonly=True)
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('archived', 'Archived'),
    ], string='Status', default='planned', required=True, tracking=True,
       index=True)
    convocation_state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('held', 'Held'),
        ('pv_done', 'Minutes Done'),
    ], string='Convocation', default='draft', required=True, tracking=True,
       index=True)
    resolution_ids = fields.One2many('sf.corporate.resolution', 'meeting_id',
                                     string='Resolutions')

    @api.depends('scheduled_date', 'org_id.notice_days',
                 'company_id.sf_corporate_default_notice_days')
    def _compute_notice_date(self):
        for meeting in self:
            days = meeting.org_id.notice_days or \
                meeting.company_id.sf_corporate_default_notice_days or 0
            meeting.notice_date = meeting.scheduled_date - timedelta(
                days=days) if meeting.scheduled_date else False

    @api.onchange('org_id')
    def _onchange_org_id(self):
        if self.org_id:
            self.company_id = self.org_id.company_id

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.corporate.meeting')
            vals['name'] = 'MEE-%s' % seq
        return super().create(vals)

    def action_start_meeting(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned meetings can be started.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only meetings in progress can be closed.'))
        if not self.minutes:
            raise UserError(_('The minutes (PV) are mandatory before the '
                              'meeting can be closed.'))
        if not self.env.user.has_group(
                'sf_corporate_secretary.group_corporate_manager'):
            raise UserError(_('Only corporate managers can close meetings.'))
        self.write({
            'state': 'done',
            'minutes_done_date': fields.Date.today(),
            'recorded_by': self.env.user.id,
        })

    def action_archive_meeting(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(_('Only done meetings can be archived.'))
        self.state = 'archived'

    def action_convocation_sent(self):
        self.ensure_one()
        if self.convocation_state != 'draft':
            raise UserError(_('Only draft convocations can be marked as '
                              'sent.'))
        self.write({'convocation_state': 'sent', 'notice_sent': True})

    def action_convocation_held(self):
        self.ensure_one()
        if self.convocation_state != 'sent':
            raise UserError(_('Only sent convocations can be marked as '
                              'held.'))
        self.convocation_state = 'held'

    def action_convocation_pv_done(self):
        self.ensure_one()
        if self.convocation_state != 'held':
            raise UserError(_('Only held convocations can be closed.'))
        if not self.minutes:
            raise UserError(_('The minutes (PV) are mandatory before the '
                              'convocation is closed.'))
        self.convocation_state = 'pv_done'

    def action_send_convocation(self):
        self.ensure_one()
        if self.convocation_state != 'draft':
            raise UserError(_('Only draft convocations can be sent.'))
        return {
            'name': _('Send Convocation'),
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'sf.corporate.meeting',
                'default_res_id': self.id,
                'default_composition_mode': 'comment',
            },
        }


class CorporateResolution(models.Model):
    _name = 'sf.corporate.resolution'
    _description = 'Corporate Resolution'
    _order = 'meeting_id, number'

    name = fields.Char(string='Number', required=True, index=True)
    meeting_id = fields.Many2one('sf.corporate.meeting', string='Meeting',
                                 required=True, ondelete='cascade',
                                 index=True)
    number = fields.Integer(string='Number', required=True)
    subject = fields.Char(string='Subject', required=True)
    vote_for = fields.Integer(string='For', default=0)
    vote_against = fields.Integer(string='Against', default=0)
    vote_abstain = fields.Integer(string='Abstain', default=0)
    adopted = fields.Boolean(string='Adopted', compute='_compute_adopted',
                             store=True, readonly=True)
    detail = fields.Text(string='Detail')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('vote_for', 'vote_against')
    def _compute_adopted(self):
        for resolution in self:
            resolution.adopted = bool(
                resolution.vote_for > resolution.vote_against)

    @api.onchange('meeting_id')
    def _onchange_meeting_id(self):
        if self.meeting_id:
            self.company_id = self.meeting_id.company_id

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.corporate.resolution')
            vals['name'] = 'RES-%s' % seq
        return super().create(vals)


class CorporateLegalDecision(models.Model):
    _name = 'sf.corporate.legal.decision'
    _description = 'Corporate Written Decision'
    _order = 'decision_date desc'

    name = fields.Char(string='Number', required=True, index=True)
    title = fields.Char(string='Title', required=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    decision_date = fields.Date(string='Decision date')
    signatory_id = fields.Many2one('res.partner', string='Signatory',
                                   ondelete='restrict')
    description = fields.Text(string='Description')
    attachment = fields.Binary(string='Attachment')
    attachment_filename = fields.Char(string='Attachment filename')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('signed', 'Signed'),
        ('filed', 'Filed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    filed_date = fields.Date(string='Filed date')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.corporate.legal.decision')
            vals['name'] = 'DEC-%s' % seq
        return super().create(vals)

    def action_sign(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft decisions can be signed.'))
        self.state = 'signed'

    def action_file(self):
        self.ensure_one()
        if self.state != 'signed':
            raise UserError(_('Only signed decisions can be filed.'))
        self.write({'state': 'filed', 'filed_date': fields.Date.today()})


class CorporateFormality(models.Model):
    _name = 'sf.corporate.formality'
    _description = 'Regulatory Formality'
    _order = 'due_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    formality_type = fields.Selection([
        ('annual_meeting', 'Annual Meeting'),
        ('financial_filing', 'Financial Filing'),
        ('statutory', 'Statutory Filing'),
        ('other', 'Other'),
    ], string='Type', default='statutory', required=True)
    due_date = fields.Date(string='Due date', required=True)
    reminder_days = fields.Integer(string='Reminder (days before)',
                                   default=30)
    done = fields.Boolean(string='Done', default=False)
    done_date = fields.Date(string='Done date')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.corporate.formality')
            vals['name'] = 'FOR-%s' % seq
        return super().create(vals)

    def action_mark_done(self):
        self.ensure_one()
        self.write({'done': True, 'done_date': fields.Date.today()})

    @api.model
    def _check_formalities(self):
        today = fields.Date.today()
        for company in self.env['res.company'].search([]):
            formalities = self.with_company(company).search([])
            for formality in formalities:
                if formality.done:
                    continue
                if formality.due_date and formality.due_date - timedelta(
                        days=formality.reminder_days or 0) <= today:
                    existing = formality.activity_ids.filtered(
                        lambda a: a.activity_type_id ==
                        self.env.ref('mail.mail_activity_data_todo')
                        and a.state != 'done')
                    if existing:
                        continue
                    formality.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Formality due: %s') % (formality.name,),
                        date_deadline=formality.due_date,
                        user_id=self.env.user.id)
            meetings = self.env['sf.corporate.meeting'].with_company(
                company).search([
                    ('state', '=', 'planned'),
                    ('notice_date', '!=', False),
                    ('notice_sent', '=', False),
                ])
            for meeting in meetings:
                if meeting.notice_date <= today:
                    existing = meeting.activity_ids.filtered(
                        lambda a: a.activity_type_id ==
                        self.env.ref('mail.mail_activity_data_todo')
                        and a.state != 'done')
                    if existing:
                        continue
                    meeting.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Send convocation: %s') % (meeting.name,),
                        date_deadline=meeting.notice_date,
                        user_id=self.env.user.id)