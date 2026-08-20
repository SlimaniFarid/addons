# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Risk(models.Model):
    _name = 'sf.risk'
    _description = 'Enterprise Risk'
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'risk_score desc'

    name = fields.Char(string='Name', required=True)
    ref = fields.Char(string='Reference', required=True,
                      default=lambda self: _('New'))
    category = fields.Selection([
        ('operational', 'Operational'),
        ('financial', 'Financial'),
        ('cyber', 'Cyber'),
        ('compliance', 'Compliance'),
        ('legal', 'Legal'),
        ('strategic', 'Strategic'),
        ('reputational', 'Reputational'),
        ('hse', 'HSE'),
    ], string='Category', required=True, tracking=True)
    source = fields.Char(string='Source')
    risk_owner_id = fields.Many2one('res.users', string='Risk Owner')
    department_id = fields.Many2one('hr.department', string='Department')
    description = fields.Text(string='Description', required=True)
    probability = fields.Integer(string='Probability', default=2)
    impact = fields.Integer(string='Impact', default=2)
    risk_score = fields.Integer(string='Risk Score',
                                compute='_compute_scores', store=True)
    risk_class = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('extreme', 'Extreme'),
    ], string='Risk Class', compute='_compute_scores', store=True)
    residual_probability = fields.Integer(string='Residual Probability',
                                          default=1)
    residual_impact = fields.Integer(string='Residual Impact', default=1)
    residual_score = fields.Integer(string='Residual Score',
                                    compute='_compute_scores', store=True)
    residual_class = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('extreme', 'Extreme'),
    ], string='Residual Class', compute='_compute_scores', store=True)
    state = fields.Selection([
        ('identified', 'Identified'),
        ('assessed', 'Assessed'),
        ('treatment_planned', 'Treatment Planned'),
        ('monitored', 'Monitored'),
        ('archived', 'Archived'),
        ('closed', 'Closed'),
    ], string='Status', default='identified', tracking=True)
    assessment_date = fields.Date(string='Assessment Date')
    actions = fields.One2many('sf.risk.action', 'risk_id',
                              string='Treatment Actions')
    controls = fields.Many2many('sf.risk.control',
                                'sf_risk_control_rel', 'risk_id',
                                'control_id', string='Controls')
    requirement_ids = fields.Many2many(
        'sf.risk.requirement',
        'sf_risk_requirement_m2m', 'risk_id', 'requirement_id',
        string='Requirements')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')

    @api.depends('probability', 'impact', 'residual_probability',
                 'residual_impact')
    def _compute_scores(self):
        for risk in self:
            risk.risk_score = risk.probability * risk.impact
            risk.risk_class = self._class_of(risk.risk_score)
            risk.residual_score = risk.residual_probability * \
                risk.residual_impact
            risk.residual_class = self._class_of(risk.residual_score)

    @api.model
    def _class_of(self, score):
        if score <= 4:
            return 'low'
        if score <= 8:
            return 'medium'
        if score <= 16:
            return 'high'
        return 'extreme'

    @api.constrains('probability', 'impact', 'residual_probability',
                    'residual_impact')
    def _check_matrix(self):
        for risk in self:
            for fname in ('probability', 'impact',
                          'residual_probability', 'residual_impact'):
                value = getattr(risk, fname)
                if value < 1 or value > 5:
                    raise UserError(
                        _('%s must be between 1 and 5.') %
                        fname.replace('_', ' ').title())

    def action_assess(self):
        for risk in self:
            if risk.state != 'identified':
                raise UserError(
                    _('Only identified risks can be assessed.'))
            if risk.risk_class in ('high', 'extreme') and \
                    not risk.risk_owner_id:
                raise UserError(
                    _('A risk owner is required for high or extreme '
                      'risks.'))
            risk.state = 'assessed'
            risk.assessment_date = fields.Date.today()
            risk.message_post(body=_('Risk assessed.'))

    def action_plan_treatment(self):
        for risk in self:
            if risk.state != 'assessed':
                raise UserError(
                    _('Only assessed risks can have a treatment plan.'))
            risk.state = 'treatment_planned'
            risk.message_post(body=_('Treatment plan defined.'))

    def action_monitor(self):
        for risk in self:
            if risk.state != 'treatment_planned':
                raise UserError(
                    _('Only risks with a treatment plan can be '
                      'monitored.'))
            done_actions = risk.actions.filtered(
                lambda a: a.state == 'done')
            if not done_actions and not risk.actions:
                raise UserError(
                    _('A treatment plan (at least one action) is '
                      'required before monitoring.'))
            risk.state = 'monitored'
            risk.message_post(body=_('Risk moved to monitoring.'))

    def action_archive(self):
        for risk in self:
            if risk.state not in ('monitored', 'assessed',
                                  'treatment_planned'):
                raise UserError(
                    _('Only active risks can be archived.'))
            risk.active = False
            risk.state = 'archived'
            risk.message_post(body=_('Risk archived.'))

    def action_close(self):
        for risk in self:
            if risk.state not in ('monitored', 'archived'):
                raise UserError(
                    _('Only monitored or archived risks can be '
                      'closed.'))
            risk.state = 'closed'
            risk.message_post(body=_('Risk closed.'))

    def unlink(self):
        for risk in self:
            if risk.active:
                raise UserError(
                    _('An active risk cannot be deleted. Archive it '
                      'instead.'))
        return super().unlink()


class RiskAction(models.Model):
    _name = 'sf.risk.action'
    _description = 'Risk Treatment Action'
    _order = 'due_date'

    risk_id = fields.Many2one('sf.risk', string='Risk',
                              ondelete='cascade', required=True)
    name = fields.Char(string='Name', required=True)
    action_type = fields.Selection([
        ('mitigate', 'Mitigate'),
        ('transfer', 'Transfer'),
        ('accept', 'Accept'),
        ('avoid', 'Avoid'),
    ], string='Type', default='mitigate')
    responsible_id = fields.Many2one('res.users', string='Responsible',
                                     required=True)
    due_date = fields.Date(string='Due Date', required=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='open', tracking=True)
    evidence = fields.Text(string='Evidence')
    closed_date = fields.Datetime(string='Closed Date')

    def action_start(self):
        for action in self:
            if action.state != 'open':
                raise UserError(_('Only open actions can be started.'))
            action.state = 'in_progress'

    def action_done(self):
        for action in self:
            if action.state != 'in_progress':
                raise UserError(
                    _('Only in-progress actions can be completed.'))
            if not action.evidence:
                raise UserError(_('Evidence is required to complete '
                                  'the action.'))
            action.state = 'done'
            action.closed_date = fields.Datetime.now()
            action.risk_id.message_post(body=_(
                'Action "%s" completed.') % action.name)

    def action_cancel(self):
        for action in self:
            if action.state not in ('open', 'in_progress'):
                raise UserError(
                    _('Only open or in-progress actions can be '
                      'cancelled.'))
            action.state = 'cancelled'