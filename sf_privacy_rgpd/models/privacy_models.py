# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PrivacyTreatment(models.Model):
    _name = 'sf.privacy.treatment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Privacy Treatment'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    title = fields.Char(string='Title', required=True)
    controller_id = fields.Many2one('res.partner', string='Controller',
                                    ondelete='restrict')
    purpose = fields.Text(string='Purpose')
    legal_basis = fields.Selection([
        ('consent', 'Consent'),
        ('contract', 'Contract'),
        ('legal', 'Legal obligation'),
        ('legitimate', 'Legitimate interest'),
        ('vital', 'Vital interest'),
    ], string='Legal basis', default='legitimate', required=True)
    lawful_basis_detail = fields.Text(string='Legal basis detail')
    data_categories = fields.Char(string='Data categories')
    retention_days = fields.Integer(string='Retention (days)')
    recipients = fields.Char(string='Recipients')
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Risk level', default='medium')
    review_frequency = fields.Integer(
        string='Review frequency (days)',
        default=lambda self: self.env.company.sf_privacy_review_days or 365)
    last_review_date = fields.Date(string='Last review date')
    next_review_date = fields.Date(string='Next review date',
                                   compute='_compute_next_review_date',
                                   store=True)
    responsible_id = fields.Many2one('res.users', string='Responsible',
                                     ondelete='restrict')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('under_review', 'Under Review'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)
    active = fields.Boolean(string='Active', default=True)
    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Attachments')

    @api.depends('last_review_date', 'review_frequency')
    def _compute_next_review_date(self):
        for treatment in self:
            if treatment.last_review_date and treatment.review_frequency:
                treatment.next_review_date = \
                    treatment.last_review_date + timedelta(
                        days=treatment.review_frequency)
            else:
                treatment.next_review_date = False

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.privacy.treatment')
            vals['name'] = 'PRT-%s' % seq
        return super().create(vals)

    def action_activate(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft treatments can be activated.'))
        self.state = 'active'

    def action_start_review(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active treatments can be put under '
                              'review.'))
        self.write({
            'state': 'under_review',
            'last_review_date': fields.Date.today(),
        })

    def action_close(self):
        self.ensure_one()
        if self.state not in ('active', 'under_review'):
            raise UserError(_('Only active or under-review treatments can be '
                              'closed.'))
        self.write({'state': 'closed', 'active': False})

    @api.model
    def _check_privacy_reviews(self):
        companies = self.env['res.company'].search([])
        now = fields.Datetime.now()
        today = fields.Date.today()
        for company in companies:
            treatments = self.with_company(company).search([
                ('state', 'in', ('active', 'under_review')),
                ('next_review_date', '!=', False),
                ('next_review_date', '<=', today)])
            for treatment in treatments:
                existing = treatment.activity_ids.filtered(
                    lambda a: a.activity_type_id.xml_id
                    == 'mail.mail_activity_data_todo' and a.state != 'done'
                    and 'review' in (a.summary or '').lower())
                if existing:
                    continue
                user = (treatment.responsible_id.user_id
                        if treatment.responsible_id
                        and treatment.responsible_id.user_id
                        else self.env.user)
                treatment.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Privacy treatment review due: %s')
                    % treatment.name,
                    user_id=user.id)
            breaches = self.env['sf.privacy.breach'].with_company(
                company).search([
                    ('state', 'in', ('detected', 'declared')),
                    ('notification_status', '!=', 'reported')])
            manager = self.env['res.users'].search(
                [('groups_id', 'in',
                  [self.env.ref(
                      'sf_privacy_rgpd.group_privacy_manager').id])],
                limit=1)
            for breach in breaches:
                if not breach.date_detected:
                    continue
                deadline = breach.date_detected + timedelta(
                    hours=company.sf_privacy_breach_hours)
                if now > deadline:
                    existing = breach.activity_ids.filtered(
                        lambda a: a.activity_type_id.xml_id
                        == 'mail.mail_activity_data_todo'
                        and a.state != 'done'
                        and ('72' in (a.summary or '')
                             or 'overdue' in (a.summary or '').lower()))
                    if existing:
                        continue
                    breach.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Breach notification overdue (72 h): %s')
                        % breach.name,
                        user_id=manager.id or self.env.user.id)


class PrivacyProcessor(models.Model):
    _name = 'sf.privacy.processor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Privacy Processor'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True, ondelete='restrict')
    contract_ref = fields.Char(string='Contract reference')
    dpa_date = fields.Date(string='DPA date')
    dpa_file = fields.Binary(string='DPA contract file')
    purpose = fields.Char(string='Purpose')
    country = fields.Char(string='Country')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)


class PrivacyImpactAssessment(models.Model):
    _name = 'sf.privacy.impact.assessment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Privacy Impact Assessment'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    treatment_id = fields.Many2one('sf.privacy.treatment',
                                   string='Treatment', required=True,
                                   ondelete='cascade')
    description = fields.Text(string='Description')
    risks = fields.Html(string='Risks')
    likelihood = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Likelihood', default='medium', required=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Severity', default='medium', required=True)
    risk_score = fields.Integer(string='Risk score',
                                compute='_compute_risk_score', store=True)
    measures = fields.Html(string='Measures')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('likelihood', 'severity')
    def _compute_risk_score(self):
        risk_map = {'low': 1, 'medium': 2, 'high': 3}
        for assessment in self:
            assessment.risk_score = \
                risk_map.get(assessment.likelihood, 0) \
                * risk_map.get(assessment.severity, 0)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code(
                'sf.privacy.impact.assessment')
            vals['name'] = 'AIP-%s' % seq
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_privacy_rgpd.group_privacy_manager'):
            raise UserError(_('Only a Privacy Manager can validate impact '
                              'assessments.'))

    def action_submit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft assessments can be submitted.'))
        self.state = 'submitted'

    def action_start_review(self):
        self.ensure_one()
        if self.state != 'submitted':
            raise UserError(_('Only submitted assessments can be reviewed.'))
        self._check_manager()
        self.state = 'in_review'

    def action_approve(self):
        self.ensure_one()
        if self.state != 'in_review':
            raise UserError(_('Only assessments under review can be '
                              'approved.'))
        self._check_manager()
        self.state = 'approved'

    def action_reject(self):
        self.ensure_one()
        if self.state != 'in_review':
            raise UserError(_('Only assessments under review can be '
                              'rejected.'))
        self._check_manager()
        self.state = 'rejected'


class PrivacyBreach(models.Model):
    _name = 'sf.privacy.breach'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Privacy Breach'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    date_detected = fields.Datetime(string='Date detected',
                                    default=fields.Datetime.now)
    description = fields.Text(string='Description', required=True)
    affected_people = fields.Integer(string='Affected people')
    categories = fields.Char(string='Data categories')
    risk = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Risk', default='medium', required=True)
    notification_status = fields.Selection([
        ('not_reported', 'Not Reported'),
        ('reported', 'Reported'),
    ], string='Notification status', default='not_reported', required=True)
    notification_date = fields.Datetime(string='Notification date')
    regulator_notified = fields.Boolean(string='Regulator notified')
    measures = fields.Text(string='Measures')
    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Attachments')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('detected', 'Detected'),
        ('declared', 'Declared'),
        ('remediated', 'Remediated'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.privacy.breach')
            vals['name'] = 'BRH-%s' % seq
        return super().create(vals)

    def action_detect(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft breaches can be detected.'))
        self.write({
            'state': 'detected',
            'date_detected': self.date_detected or fields.Datetime.now(),
        })

    def action_declare(self):
        self.ensure_one()
        if self.state != 'detected':
            raise UserError(_('Only detected breaches can be declared.'))
        self.write({
            'state': 'declared',
            'notification_status': 'reported',
            'notification_date': fields.Datetime.now(),
        })

    def action_remediate(self):
        self.ensure_one()
        if self.state != 'declared':
            raise UserError(_('Only declared breaches can be remediated.'))
        self.state = 'remediated'

    def action_close(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_privacy_rgpd.group_privacy_manager'):
            raise UserError(_('Only privacy managers can close breaches.'))
        if self.state != 'remediated':
            raise UserError(_('Only remediated breaches can be closed.'))
        if not self.measures:
            raise UserError(_('Remediation measures are required before a '
                              'breach can be closed.'))
        self.state = 'closed'


class PrivacyRequest(models.Model):
    _name = 'sf.privacy.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Privacy Request'
    _order = 'id desc'

    name = fields.Char(string='Number', required=True, index=True)
    request_type = fields.Selection([
        ('access', 'Access'),
        ('rectification', 'Rectification'),
        ('erasure', 'Erasure'),
        ('portability', 'Portability'),
        ('objection', 'Objection'),
        ('other', 'Other'),
    ], string='Request type', required=True)
    person_name = fields.Char(string='Person name', required=True)
    contact = fields.Char(string='Contact')
    treatment_id = fields.Many2one('sf.privacy.treatment',
                                   string='Treatment', ondelete='restrict')
    request_date = fields.Date(string='Request date',
                               default=fields.Date.today, required=True)
    deadline = fields.Date(string='Deadline')
    response_date = fields.Date(string='Response date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.privacy.request')
            vals['name'] = 'REQ-%s' % seq
        return super().create(vals)

    def action_start(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft requests can be started.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress requests can be marked as '
                              'done.'))
        self.write({
            'state': 'done',
            'response_date': self.response_date or fields.Date.today(),
        })

    def action_close(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(_('Only done requests can be closed.'))
        self.state = 'closed'