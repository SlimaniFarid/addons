# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ApprovalTemplate(models.Model):
    _name = 'sf.approval.template'
    _description = 'Approval Template'
    _order = 'sequence asc, id asc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Template Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)
    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        help='The Odoo model this template applies to, e.g. purchase.order.',
    )
    model_name = fields.Char(
        string='Model Name',
        related='model_id.model',
        readonly=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    note = fields.Text(string='Description')

    step_ids = fields.One2many(
        'sf.approval.step',
        'template_id',
        string='Approval Steps',
    )
    approval_request_ids = fields.One2many(
        'sf.approval.request',
        'template_id',
        string='Approval Requests',
    )

    @api.constrains('step_ids')
    def _check_steps(self):
        for template in self:
            if template.step_ids:
                sequences = template.step_ids.mapped('sequence')
                if len(sequences) != len(set(sequences)):
                    raise ValidationError(
                        _('Approval step sequences must be unique.'))
                if min(sequences) != 1:
                    raise ValidationError(
                        _('Approval step sequence must start at 1.'))


class ApprovalStep(models.Model):
    _name = 'sf.approval.step'
    _description = 'Approval Step'
    _order = 'sequence asc, id asc'

    template_id = fields.Many2one(
        'sf.approval.template',
        string='Template',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(string='Step', default=1, required=True)
    name = fields.Char(string='Step Name', required=True, translate=True)
    assignment = fields.Selection(
        [
            ('specific', 'Specific user'),
            ('manager', 'Manager of requester'),
            ('group', 'Any user of a group'),
            ('any_approver', 'Any approver of the template'),
        ],
        string='Assignment',
        required=True,
        default='manager',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Approver',
        help='Used when assignment is "specific user".',
    )
    group_id = fields.Many2one(
        'res.groups',
        string='Group',
        help='Used when assignment is "any user of a group".',
    )
    is_auto_approve = fields.Boolean(
        string='Auto-approve when not applicable',
        help='If the amount is below the threshold, approve this step '
             'automatically and skip to the next.',
    )
    min_amount = fields.Monetary(
        string='Minimum Amount',
        currency_field='currency_id',
        help='Step only applies when the document amount reaches this value.',
    )
    max_amount = fields.Monetary(
        string='Maximum Amount',
        currency_field='currency_id',
        help='Step only applies when the document amount is below this value.',
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='template_id.company_id.currency_id',
        readonly=True,
    )
    required = fields.Boolean(
        string='Always required',
        default=True,
        help='If disabled, the step can be skipped when the rules match.',
    )

    @api.onchange('assignment')
    def _onchange_assignment(self):
        if self.assignment != 'specific':
            self.user_id = False
        if self.assignment != 'group':
            self.group_id = False

    def _is_applicable(self, record):
        self.ensure_one()
        if not self.required:
            return False
        amount = self._get_document_amount(record)
        if self.min_amount and amount < self.min_amount:
            return False
        if self.max_amount and amount >= self.max_amount:
            return False
        return True

    def _get_document_amount(self, record):
        for field in ('amount_total', 'total_amount', 'amount'):
            if field in record._fields:
                value = getattr(record, field)
                if value:
                    return value
        return 0.0

    def _resolve_approvers(self, record, requester):
        self.ensure_one()
        if self.assignment == 'specific':
            return self.user_id
        if self.assignment == 'manager':
            if requester.parent_id:
                return requester.parent_id
            return requester
        if self.assignment == 'group':
            return self.group_id.users
        return self.template_id.approval_request_ids.mapped(
            'approver_ids').filtered(lambda u: u != requester)


class ApprovalRequest(models.Model):
    _name = 'sf.approval.request'
    _description = 'Approval Request'
    _order = 'create_date desc, id desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Reference', required=True, copy=False)
    template_id = fields.Many2one(
        'sf.approval.template',
        string='Template',
        required=True,
        ondelete='restrict',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )
    res_model = fields.Char(string='Related Model', readonly=True)
    res_id = fields.Integer(string='Related Record', readonly=True)
    document_name = fields.Char(string='Document')
    amount = fields.Monetary(
        string='Amount',
        currency_field='currency_id',
    )
    requester_id = fields.Many2one(
        'res.users',
        string='Requester',
        required=True,
        default=lambda self: self.env.user,
        readonly=True,
    )
    date_requested = fields.Datetime(
        string='Requested On',
        default=fields.Datetime.now,
        readonly=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    current_step_id = fields.Many2one(
        'sf.approval.step',
        string='Current Step',
        readonly=True,
    )
    approver_ids = fields.Many2many(
        'res.users',
        string='Approvers',
        tracking=True,
    )
    current_approver_ids = fields.Many2many(
        'res.users',
        string='Current Approvers',
        compute='_compute_current_approvers',
    )
    step_history_ids = fields.One2many(
        'sf.approval.history',
        'request_id',
        string='Approval History',
    )
    reason = fields.Text(string='Reason / Comment')
    rejected_reason = fields.Text(string='Rejection Reason')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.approval.request')
        return super().create(vals_list)

    @api.depends('approver_ids', 'state')
    def _compute_current_approvers(self):
        for request in self:
            if request.state != 'submitted':
                request.current_approver_ids = [(5, 0, 0)]
                continue
            if request.approver_ids:
                request.current_approver_ids = [
                    (6, 0, request.approver_ids.ids)]
            else:
                request.current_approver_ids = [(5, 0, 0)]

    def _prepare_steps(self):
        self.ensure_one()
        if not self.res_model or not self.res_id:
            return self.template_id.step_ids
        record = self.env[self.res_model].browse(self.res_id)
        return self.template_id.step_ids.filtered(
            lambda step: step._is_applicable(record))

    def action_submit(self):
        steps = self._prepare_steps()
        if not steps:
            self.write({'state': 'approved'})
            return True
        first = steps[0]
        approvers = first._resolve_approvers(
            self._get_document_record(), self.requester_id)
        self.write({
            'state': 'submitted',
            'current_step_id': first.id,
            'approver_ids': [(6, 0, approvers.ids)],
        })
        return True

    def action_approve(self):
        self.ensure_one()
        if self.env.user not in self.approver_ids:
            raise ValidationError(
                _('You are not an approver for this request.'))
        self.env['sf.approval.history'].create({
            'request_id': self.id,
            'step_id': self.current_step_id.id,
            'user_id': self.env.user.id,
            'action': 'approved',
            'date': fields.Datetime.now(),
        })
        steps = self._prepare_steps()
        steps = steps.filtered(
            lambda s: s.sequence > self.current_step_id.sequence)
        if not steps:
            self.write({'state': 'approved'})
            return True
        next_step = steps[0]
        approvers = next_step._resolve_approvers(
            self._get_document_record(), self.requester_id)
        self.write({
            'current_step_id': next_step.id,
            'approver_ids': [(6, 0, approvers.ids)],
        })
        return True

    def action_reject(self, reason=None):
        self.ensure_one()
        if self.env.user not in self.approver_ids:
            raise ValidationError(
                _('You are not an approver for this request.'))
        self.env['sf.approval.history'].create({
            'request_id': self.id,
            'step_id': self.current_step_id.id,
            'user_id': self.env.user.id,
            'action': 'rejected',
            'reason': reason or self.rejected_reason,
            'date': fields.Datetime.now(),
        })
        self.write({
            'state': 'rejected',
            'rejected_reason': reason or self.rejected_reason,
        })
        return True

    def action_draft(self):
        self.write({'state': 'draft', 'approver_ids': [(5, 0, 0)]})
        return True

    def _get_document_record(self):
        if not self.res_model or not self.res_id:
            return self.env['res.users']
        return self.env[self.res_model].browse(self.res_id)


class ApprovalHistory(models.Model):
    _name = 'sf.approval.history'
    _description = 'Approval History Entry'
    _order = 'date desc, id desc'

    request_id = fields.Many2one(
        'sf.approval.request',
        string='Request',
        required=True,
        ondelete='cascade',
    )
    step_id = fields.Many2one(
        'sf.approval.step',
        string='Step',
    )
    step_name = fields.Char(string='Step Name', readonly=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    action = fields.Selection(
        [
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Action',
        required=True,
    )
    reason = fields.Text(string='Reason')
    date = fields.Datetime(string='Date', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('step_id'):
                step = self.env['sf.approval.step'].browse(vals['step_id'])
                vals['step_name'] = step.name
        return super().create(vals_list)