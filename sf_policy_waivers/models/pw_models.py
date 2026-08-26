# -*- coding: utf-8 -*-
"""Policy waiver requests."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPolicyWaiver(models.Model):
    _name = 'sf.policy.waiver'
    _description = 'Policy Waiver Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'valid_to desc'

    name = fields.Char(string='Waiver Reference', required=True, copy=False,
                       readonly=True, default='New')
    policy_name = fields.Char(string='Policy / Rule Waived', required=True)
    requester_id = fields.Many2one('res.users', string='Requested By',
                                   default=lambda s: s.env.uid)
    department = fields.Char(string='Department')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    reason = fields.Text(string='Justification / Reason', required=True)
    risk_level = fields.Selection([
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        required=True, default='medium')
    risk_assessment = fields.Text(string='Risk Assessment')
    compensating_controls = fields.Text(string='Compensating Controls',
                                        required=True)
    valid_from = fields.Date(string='Valid From', required=True,
                             default=fields.Date.today)
    valid_to = fields.Date(string='Valid To', required=True)
    approver_id = fields.Many2one('res.users', string='Approved By',
                                  readonly=True)
    decision_date = fields.Date(readonly=True)
    rejection_reason = fields.Text(string='Rejection Reason')
    expired = fields.Boolean(string='Expired',
                             compute='_compute_expired', store=True)
    state = fields.Selection([
        ('requested', 'Requested'), ('approved', 'Approved'),
        ('rejected', 'Rejected'), ('cancelled', 'Cancelled')],
        default='requested', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.policy.waiver') or 'WAIV-NEW'
        return super().create(vals_list)

    def _compute_expired(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.expired = (rec.state == 'approved' and rec.valid_to
                           and rec.valid_to < today)

    @api.constrains('valid_from', 'valid_to')
    def _check_dates(self):
        for rec in self:
            if rec.valid_to and rec.valid_from and rec.valid_to < rec.valid_from:
                raise UserError(_('Valid To must be after Valid From.'))

    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved', 'approver_id': rec.env.uid,
                       'decision_date': fields.Date.today()})

    def action_reject(self):
        for rec in self:
            if not rec.rejection_reason:
                raise UserError(_('Provide a rejection reason.'))
            rec.write({'state': 'rejected', 'approver_id': rec.env.uid,
                       'decision_date': fields.Date.today()})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.policy.waiver'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
