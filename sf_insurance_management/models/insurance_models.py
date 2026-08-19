# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, UserWarning, ValidationError


class InsuranceCompany(models.Model):
    _name = 'sf.insurance.company'
    _description = 'Insurance Company'
    _order = 'name'

    name = fields.Char(string='Name', index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 ondelete='restrict')
    reference = fields.Char(string='Reference')
    rating = fields.Char(string='Rating')
    policy_ids = fields.One2many('sf.insurance.policy', 'insurer_id',
                                 string='Policies', copy=False)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.insurance.company')
        return super().create(vals)


class InsurancePolicy(models.Model):
    _name = 'sf.insurance.policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Insurance Policy'
    _order = 'end_date desc'

    name = fields.Char(string='Number', index=True)
    policy_number = fields.Char(string='Policy number', index=True)
    insurer_id = fields.Many2one('sf.insurance.company', string='Insurer',
                                 required=True, ondelete='restrict',
                                 index=True)
    policy_type = fields.Selection([
        ('liability', 'Liability'),
        ('property', 'Property'),
        ('fleet', 'Fleet'),
        ('life', 'Life'),
        ('health', 'Health'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ], string='Type', required=True)
    start_date = fields.Date(string='Start date', required=True)
    end_date = fields.Date(string='End date', index=True)
    auto_renew = fields.Boolean(string='Automatic renewal', default=True)
    premium_amount = fields.Float(string='Premium amount')
    premium_frequency = fields.Selection([
        ('annual', 'Annual'),
        ('semi_annual', 'Semi-Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly'),
    ], string='Premium frequency', default='annual')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self:
                                  self.env.company.currency_id)
    coverage = fields.Html(string='Coverage')
    guarantee_ids = fields.One2many('sf.insurance.guarantee', 'policy_id',
                                    string='Guarantees')
    claim_ids = fields.One2many('sf.insurance.claim', 'policy_id',
                                string='Claims', copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('under_review', 'Under Review'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.insurance.policy')
        if not vals.get('policy_number'):
            vals['policy_number'] = vals['name']
        return super().create(vals)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for policy in self:
            if policy.start_date and policy.end_date and \
                    policy.end_date < policy.start_date:
                raise ValidationError(_('End date cannot be before the '
                                        'start date.'))

    def action_activate(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft policies can be activated.'))
        self.state = 'active'

    def action_under_review(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active policies can be put under '
                              'review.'))
        self.state = 'under_review'

    def action_expire(self):
        self.ensure_one()
        if self.state not in ('active', 'under_review'):
            raise UserError(_('Only active or under review policies can be '
                              'expired.'))
        self.state = 'expired'

    def action_cancel(self):
        self.ensure_one()
        if self.state not in ('draft', 'active', 'under_review'):
            raise UserError(_('Only non-terminal policies can be '
                              'cancelled.'))
        self.state = 'cancelled'

    def _get_period_days(self):
        self.ensure_one()
        return {
            'annual': 365,
            'semi_annual': 182,
            'quarterly': 91,
            'monthly': 30,
        }.get(self.premium_frequency, 365)

    @api.model
    def _sub_working_days(self, date, days):
        current = date
        remaining = days
        while remaining > 0:
            current -= timedelta(days=1)
            if current.weekday() < 5:
                remaining -= 1
        return current

    @api.model
    def _check_policies(self):
        companies = self.env['res.company'].search([])
        today = fields.Date.today()
        for company in companies:
            remind_days = company.sf_insurance_remind_days or 0
            policies = self.search([
                ('company_id', '=', company.id),
                ('state', 'in', ('active', 'under_review')),
                ('end_date', '!=', False),
            ])
            for policy in policies:
                if policy.end_date < today:
                    if policy.auto_renew:
                        policy.copy(default={
                            'name': False,
                            'policy_number': policy.policy_number,
                            'start_date': policy.end_date,
                            'end_date': policy.end_date + timedelta(
                                days=policy._get_period_days()),
                            'state': 'active',
                            'premium_frequency': policy.premium_frequency,
                            'company_id': policy.company_id.id,
                        })
                    policy.state = 'expired'
                else:
                    reminder_date = policy.end_date - timedelta(
                        days=remind_days)
                    if reminder_date <= today:
                        existing = policy.activity_ids.filtered(
                            lambda a: a.activity_type_id ==
                            self.env.ref('mail.mail_activity_data_todo')
                            and a.state != 'done')
                        if existing:
                            continue
                        policy.activity_schedule(
                            'mail.mail_activity_data_todo',
                            summary=_('Policy %s renewal due')
                            % (policy.name,),
                            user_id=self.env.user.id)
            cutoff = self._sub_working_days(today, 5)
            pending = self.env['sf.insurance.claim'].search([
                ('company_id', '=', company.id),
                ('state', '=', 'draft'),
            ])
            for claim in pending:
                ref_date = claim.date_notified or claim.date_occurred
                if ref_date and ref_date < cutoff:
                    existing = claim.activity_ids.filtered(
                        lambda a: a.activity_type_id.xml_id ==
                        'mail.mail_activity_data_todo' and a.state != 'done')
                    if existing:
                        continue
                    claim.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Claim %s awaiting declaration')
                        % (claim.name,),
                        user_id=self.env.user.id)


class InsuranceGuarantee(models.Model):
    _name = 'sf.insurance.guarantee'
    _description = 'Insurance Guarantee'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    policy_id = fields.Many2one('sf.insurance.policy', string='Policy',
                                required=True, ondelete='cascade',
                                index=True)
    guarantee_type = fields.Char(string='Guarantee type')
    coverage_amount = fields.Float(string='Coverage amount')
    deductible = fields.Float(string='Deductible')
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='policy_id.company_id', store=True,
                                 readonly=True)


class InsuranceClaim(models.Model):
    _name = 'sf.insurance.claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Insurance Claim'
    _order = 'date_occurred desc'

    name = fields.Char(string='Number', index=True)
    claim_number = fields.Char(string='Claim number', index=True)
    policy_id = fields.Many2one('sf.insurance.policy', string='Policy',
                                required=True, ondelete='cascade',
                                index=True)
    date_occurred = fields.Date(string='Date occurred', required=True)
    date_notified = fields.Date(string='Date notified')
    description = fields.Text(string='Description')
    estimated_amount = fields.Float(string='Estimated amount')
    settlement_amount = fields.Float(string='Settlement amount')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('declared', 'Declared'),
        ('under_review', 'Under Review'),
        ('estimated', 'Estimated'),
        ('settled', 'Settled'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    closed_date = fields.Date(string='Closed date')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.insurance.claim')
        if not vals.get('claim_number'):
            vals['claim_number'] = vals['name']
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_insurance_management.group_insurance_manager'):
            raise UserError(_('Only insurance managers can settle or reject '
                              'claims.'))

    def action_declare(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft claims can be declared.'))
        if not self.date_notified:
            self.date_notified = fields.Date.today()
        self.state = 'declared'

    def action_review(self):
        self.ensure_one()
        if self.state != 'declared':
            raise UserError(_('Only declared claims can be put under '
                              'review.'))
        self.state = 'under_review'

    def action_estimate(self):
        self.ensure_one()
        if self.state != 'under_review':
            raise UserError(_('Only claims under review can be estimated.'))
        if not self.estimated_amount:
            raise UserError(_('An estimated amount is required to estimate '
                              'the claim.'))
        self.state = 'estimated'

    def action_settle(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'estimated':
            raise UserError(_('Only estimated claims can be settled.'))
        if not self.settlement_amount:
            raise UserError(_('A settlement amount is required to settle '
                              'the claim.'))
        if self.estimated_amount and \
                self.settlement_amount > self.estimated_amount:
            raise UserWarning(_('The settlement amount exceeds the estimated '
                                'amount.'))
        self.write({'state': 'settled',
                    'closed_date': fields.Date.today()})

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state not in ('declared', 'under_review', 'estimated'):
            raise UserError(_('Only claims in progress can be rejected.'))
        if not self.notes:
            raise UserError(_('A reason in the notes field is required to '
                              'reject a claim.'))
        self.write({'state': 'rejected',
                    'closed_date': fields.Date.today()})
