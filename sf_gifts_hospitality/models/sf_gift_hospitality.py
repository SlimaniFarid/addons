# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfGiftHospitality(models.Model):
    _name = 'sf.gift.hospitality'
    _description = 'Gift & Hospitality Declaration'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.gift.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    employee_id = fields.Many2one(
        'res.users', string='Employee',
        default=lambda self: self.env.user, required=True)
    direction = fields.Selection([
        ('given', 'Given'),
        ('received', 'Received'),
    ], string='Direction', required=True)
    counterparty_id = fields.Many2one('res.partner', string='Counterparty')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    category = fields.Selection([
        ('gift', 'Gift'),
        ('meal', 'Meal'),
        ('event', 'Event'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ], string='Category', required=True, default='gift')
    description = fields.Text(string='Description', required=True)
    estimated_value = fields.Monetary(
        string='Estimated Value', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        related='company_id.currency_id', readonly=True, store=True)
    justification = fields.Text(string='Justification')
    requires_approval = fields.Boolean(
        string='Approval Required', compute='_compute_requires_approval')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', copy=False)
    approved_by = fields.Many2one('res.users', string='Approved By')
    approved_date = fields.Date(string='Approved Date')
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    @api.depends('estimated_value', 'company_id')
    def _compute_requires_approval(self):
        for record in self:
            threshold = record._get_approval_threshold()
            record.requires_approval = (
                record.estimated_value or 0.0) >= threshold

    @api.model
    def _get_approval_threshold(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_gifts_hospitality.approval_threshold')
        return float(param) if param else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.gift.hospitality')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group(
                'sf_gifts_hospitality.group_sf_gifts_hospitality_manager'):
            raise UserError(_('Only a compliance manager can perform this action.'))

    def _set_state(self, state):
        self.ensure_one()
        self.with_context(sf_gift_bypass_state=True).write({'state': state})

    def write(self, vals):
        if 'state' in vals and not self.env.context.get('sf_gift_bypass_state'):
            raise UserError(_('The status cannot be modified directly.'))
        if 'estimated_value' in vals:
            for record in self:
                if record.state not in ('draft', 'submitted'):
                    raise UserError(_('The estimated value can only be modified while the declaration is in draft or submitted.'))
        return super().write(vals)

    def action_submit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft declarations can be submitted.'))
        if self.requires_approval:
            self._set_state('submitted')
            self._sf_check_todo(
                self.env.ref('mail.mail_activity_data_todo').id,
                _('Declaration submitted for approval: %s', self.name),
                _('Please review this gift/hospitality declaration.')
            )
        else:
            self.write({
                'approved_by': self.env.user.id,
                'approved_date': fields.Date.context_today(self),
            })
            self._set_state('approved')
            self._sf_check_todo(
                self.env.ref('mail.mail_activity_data_todo').id,
                _('Declaration auto-approved: %s', self.name),
                _('Declaration was auto-approved as it is below the approval threshold.')
            )

    def action_approve(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'submitted':
            raise UserError(_('Only submitted declarations can be approved.'))
        self.write({
            'approved_by': self.env.user.id,
            'approved_date': fields.Date.context_today(self),
        })
        self._set_state('approved')
        self._sf_check_todo(
            self.env.ref('mail.mail_activity_data_todo').id,
            _('Declaration approved: %s', self.name),
            _('Your declaration has been approved.')
        )

    def action_reject(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'submitted':
            raise UserError(_('Only submitted declarations can be rejected.'))
        self._set_state('rejected')
        self._sf_check_todo(
            self.env.ref('mail.mail_activity_data_todo').id,
            _('Declaration rejected: %s', self.name),
            _('Your declaration has been rejected. Please review and resubmit if needed.')
        )

    def action_resubmit(self):
        self.ensure_one()
        if self.state != 'rejected':
            raise UserError(_('Only rejected declarations can be resubmitted.'))
        self._set_state('submitted')
        self._sf_check_todo(
            self.env.ref('mail.mail_activity_data_todo').id,
            _('Declaration resubmitted: %s', self.name),
            _('Please review this gift/hospitality declaration.')
        )

    def action_archive(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'approved':
            raise UserError(_('Only approved declarations can be archived.'))
        self._set_state('archived')
        self._sf_check_todo(
            self.env.ref('mail.mail_activity_data_todo').id,
            _('Declaration archived: %s', self.name),
            _('This declaration has been archived.')
        )

    def _declaration_lines(self):
        grouped = {}
        today = fields.Date.context_today(self)
        for record in self:
            date = record.date or today
            year = date.year
            key = (record.employee_id.id, year)
            grouped.setdefault(key, []).append(record)
        lines = []
        for (employee_id, year), records in sorted(grouped.items()):
            lines.append({
                'employee': records[0].employee_id.name,
                'year': year,
                'records': records,
                'total': sum((r.estimated_value or 0.0) for r in records),
            })
        return lines