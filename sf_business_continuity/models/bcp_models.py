# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBcpProcess(models.Model):
    _name = 'sf.bcp.process'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Business Continuity Process / BIA'
    _order = 'criticality, name'

    name = fields.Char(string='Number', required=True, index=True)
    department_id = fields.Char(string='Department')
    criticality = fields.Selection([
        ('critical', 'Critical'),
        ('important', 'Important'),
        ('normal', 'Normal'),
    ], string='Criticality', required=True, default='normal',
       tracking=True, index=True)
    rto = fields.Integer(string='RTO (hours)')
    rpo = fields.Integer(string='RPO (hours)')
    impact = fields.Float(string='Financial impact')
    dependencies = fields.Char(string='Dependencies')
    strategy_ids = fields.One2many('sf.bcp.strategy', 'process_id',
                                   string='Strategies')
    plan_ids = fields.One2many('sf.bcp.plan', 'process_id',
                               string='Recovery plans')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assessed', 'Assessed'),
        ('validated', 'Validated'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.bcp.process')
        return super().create(vals)

    def action_assess(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft processes can be assessed.'))
        self.state = 'assessed'

    def action_validate(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_business_continuity.group_bcp_manager'):
            raise UserError(_('Only a BCP manager can validate the BIA.'))
        if self.state != 'assessed':
            raise UserError(_('Only assessed processes can be validated.'))
        self.state = 'validated'

    def action_archive(self):
        self.ensure_one()
        if self.state != 'validated':
            raise UserError(_('Only validated processes can be archived.'))
        self.state = 'archived'


class SfBcpStrategy(models.Model):
    _name = 'sf.bcp.strategy'
    _description = 'Business Continuity Strategy'
    _order = 'process_id, name'

    name = fields.Char(string='Number', required=True, index=True)
    process_id = fields.Many2one('sf.bcp.process', string='Process',
                                 required=True, ondelete='restrict',
                                 index=True)
    strategy_type = fields.Selection([
        ('alternate_site', 'Alternate Site'),
        ('workaround', 'Workaround'),
        ('outsourcing', 'Outsourcing'),
        ('manual', 'Manual Procedure'),
        ('staffing', 'Staffing'),
    ], string='Strategy type', required=True)
    detail = fields.Char(string='Detail')
    cost = fields.Float(string='Cost')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.bcp.strategy')
        return super().create(vals)


class SfBcpPlan(models.Model):
    _name = 'sf.bcp.plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Business Continuity Recovery Plan'
    _order = 'next_review_date, name'

    name = fields.Char(string='Number', required=True, index=True)
    process_id = fields.Many2one('sf.bcp.process', string='Process',
                                 required=True, ondelete='restrict',
                                 index=True)
    version = fields.Char(string='Version', default='1.0')
    summary = fields.Html(string='Summary')
    owner_id = fields.Many2one('res.partner', string='Plan owner',
                               ondelete='restrict')
    resource_ids = fields.Char(string='Resources')
    steps = fields.Html(string='Recovery steps')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('tested', 'Tested'),
        ('updated', 'Updated'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    published_date = fields.Date(string='Published date', index=True)
    last_review_date = fields.Date(string='Last review date')
    next_review_date = fields.Date(string='Next review date',
                                   compute='_compute_next_review_date',
                                   store=True, index=True)
    exercise_ids = fields.One2many('sf.bcp.exercise', 'plan_id',
                                   string='Exercises')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.bcp.plan')
        return super().create(vals)

    @api.depends('last_review_date', 'published_date', 'company_id',
                 'company_id.sf_bcp_review_days')
    def _compute_next_review_date(self):
        for plan in self:
            base = plan.last_review_date or plan.published_date
            if base:
                days = plan.company_id.sf_bcp_review_days or 365
                plan.next_review_date = base + timedelta(days=days)
            else:
                plan.next_review_date = False

    def action_publish(self):
        self.ensure_one()
        if not self.env.user.has_group(
                'sf_business_continuity.group_bcp_manager'):
            raise UserError(_('Only a BCP manager can publish plans.'))
        if self.state != 'draft':
            raise UserError(_('Only draft plans can be published.'))
        if not self.summary or not self.steps:
            raise UserError(_('A plan must have a summary and recovery '
                              'steps before being published.'))
        today = fields.Date.today()
        self.write({
            'state': 'published',
            'published_date': today,
            'last_review_date': today,
        })

    def action_mark_tested(self):
        self.ensure_one()
        if self.state != 'published':
            raise UserError(_('Only published plans can be marked as '
                              'tested.'))
        self.state = 'tested'

    def action_update(self):
        self.ensure_one()
        if self.state != 'tested':
            raise UserError(_('Only tested plans can be updated.'))
        self.state = 'updated'
        self.last_review_date = fields.Date.today()

    @api.model
    def _check_bcp_reviews(self):
        companies = self.env['res.company'].search([])
        today = fields.Date.today()
        for company in companies:
            plans = self.search([
                ('company_id', '=', company.id),
                ('state', '!=', 'draft'),
                ('next_review_date', '!=', False),
                ('next_review_date', '<=', today),
            ])
            for plan in plans:
                existing = plan.activity_ids.filtered(
                    lambda a: a.activity_type_id ==
                    self.env.ref('mail.mail_activity_data_todo')
                    and a.state != 'done')
                if existing:
                    continue
                plan.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Recovery plan %s review due') % (plan.name,),
                    user_id=self.env.user.id)


class SfBcpExercise(models.Model):
    _name = 'sf.bcp.exercise'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Business Continuity Exercise'
    _order = 'exercise_date desc'

    name = fields.Char(string='Number', required=True, index=True)
    plan_id = fields.Many2one('sf.bcp.plan', string='Recovery plan',
                              required=True, ondelete='restrict',
                              index=True)
    exercise_date = fields.Date(string='Exercise date', index=True)
    scenario = fields.Text(string='Scenario')
    participants = fields.Char(string='Participants')
    objectives = fields.Text(string='Objectives')
    results = fields.Html(string='Results')
    findings = fields.Text(string='Improvement findings')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('executed', 'Executed'),
        ('done', 'Done'),
    ], string='Status', default='planned', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.bcp.exercise')
        return super().create(vals)

    def action_execute(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned exercises can be executed.'))
        self.state = 'executed'

    def action_done(self):
        self.ensure_one()
        if self.state != 'executed':
            raise UserError(_('Only executed exercises can be closed.'))
        if not self.results:
            raise UserError(_('An exercise requires results before being '
                              'closed.'))
        self.state = 'done'