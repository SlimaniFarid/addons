# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfTradeClaim(models.Model):
    _name = 'sf.trade.claim'
    _description = 'Trade Promotion Claim'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.trade.promotions.activity.mixin']
    _order = 'claim_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    program_id = fields.Many2one('sf.trade.program', string='Trade Program', required=True,
                                 ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True,
                                 ondelete='restrict')
    invoice_id = fields.Many2one('account.move', string='Related Invoice', ondelete='set null')
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    reason = fields.Char(string='Reason')
    claim_date = fields.Date(string='Claim Date',
                             default=lambda self: fields.Date.context_today(self))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('amount_positive', 'CHECK (amount > 0)', 'The claim amount must be positive.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.trade.claim')
            if not vals.get('company_id') and vals.get('program_id'):
                program = self.env['sf.trade.program'].browse(vals['program_id'])
                vals['company_id'] = program.company_id.id
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_trade_promotions.group_sf_trade_promotions_manager'):
            raise UserError(_('Only a trade promotions manager can perform this action.'))

    def action_submit(self):
        for claim in self:
            if claim.state != 'draft':
                raise UserError(_('Only draft claims can be submitted.'))
            if claim.program_id.state != 'active':
                raise UserError(_('Claims can only be submitted for active programs.'))
            claim.state = 'submitted'
            claim.message_post(body=_('The claim was submitted for validation.'))
            threshold = float(self.env['ir.config_parameter'].sudo().get_param(
                'sf_trade_promotions.validation_threshold', '0'))
            if threshold > 0 and claim.amount > threshold:
                claim._sf_check_todo(
                    self.env.ref('mail.mail_activity_data_todo'),
                    _('Claim %s exceeds the validation threshold') % claim.name,
                    _('Review this claim carefully before approving it.'),
                )

    def action_approve(self):
        self._check_manager()
        for claim in self:
            if claim.state != 'submitted':
                raise UserError(_('Only submitted claims can be approved.'))
            if claim.amount > claim.program_id.remaining_budget:
                raise UserError(_('Approving this claim would exceed the remaining budget '
                                  'of the program.'))
            claim.state = 'approved'
            claim.message_post(body=_('The claim was approved.'))

    def action_reject(self):
        self._check_manager()
        for claim in self:
            if claim.state != 'submitted':
                raise UserError(_('Only submitted claims can be rejected.'))
            claim.state = 'rejected'
            claim.message_post(body=_('The claim was rejected.'))

    def action_mark_paid(self):
        self._check_manager()
        for claim in self:
            if claim.state != 'approved':
                raise UserError(_('Only approved claims can be marked as paid.'))
            claim.state = 'paid'
            claim.message_post(body=_('The claim was marked as paid.'))

    def action_cancel(self):
        self._check_manager()
        for claim in self:
            if claim.state in ('approved', 'paid'):
                raise UserError(_('Approved or paid claims cannot be cancelled.'))
            claim.state = 'cancelled'
            claim.message_post(body=_('The claim was cancelled.'))