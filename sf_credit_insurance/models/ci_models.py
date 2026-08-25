# -*- coding: utf-8 -*-
"""Credit insurance policies, buyer limits and claims."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCiPolicy(models.Model):
    _name = 'sf.ci.policy'
    _description = 'Credit Insurance Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Policy Reference', required=True, copy=False,
                       readonly=True, default='New')
    insurer_id = fields.Many2one('res.partner', string='Insurer',
                                 required=True)
    policy_number = fields.Char(string='Policy Number')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    date_start = fields.Date(string='Start', required=True,
                             default=fields.Date.today)
    date_end = fields.Date(string='End', required=True)
    default_coverage_percent = fields.Float(string='Default Coverage %',
                                            default=90.0)
    premium_percent = fields.Float(string='Premium % (of insured turnover)')
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'),
                              ('expired', 'Expired')], default='draft',
                             tracking=True)
    buyer_ids = fields.One2many('sf.ci.buyer', 'policy_id',
                                string='Insured Buyers')
    claim_ids = fields.One2many('sf.ci.claim', 'policy_id', string='Claims')
    buyer_count = fields.Integer(compute='_compute_counts')
    claim_count = fields.Integer(compute='_compute_counts')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.ci.policy') or 'CIP-NEW'
        return super().create(vals_list)

    def _compute_counts(self):
        for rec in self:
            rec.buyer_count = len(rec.buyer_ids)
            rec.claim_count = len(rec.claim_ids)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_expire(self):
        self.write({'state': 'expired'})


class SfCiBuyer(models.Model):
    _name = 'sf.ci.buyer'
    _description = 'Insured Buyer Limit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    policy_id = fields.Many2one('sf.ci.policy', string='Policy',
                                required=True, ondelete='cascade')
    company_id = fields.Many2one(related='policy_id.company_id', store=True)
    currency_id = fields.Many2one(related='policy_id.currency_id')
    partner_id = fields.Many2one('res.partner', string='Buyer',
                                 required=True)
    requested_limit = fields.Monetary(string='Requested Limit', required=True)
    approved_limit = fields.Monetary(string='Approved Limit')
    coverage_percent = fields.Float(string='Coverage %')
    decision_date = fields.Date(string='Decision Date', readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'), ('approved', 'Approved'),
        ('reduced', 'Reduced'), ('rejected', 'Rejected')],
        default='pending', tracking=True)
    notes = fields.Text(string='Insurer Notes')

    def action_mark_approved(self):
        for rec in self:
            if not rec.approved_limit:
                rec.approved_limit = rec.requested_limit
            rec.write({'state': 'approved', 'coverage_percent':
                       rec.coverage_percent or
                       rec.policy_id.default_coverage_percent,
                       'decision_date': fields.Date.today()})

    def action_mark_reduced(self):
        for rec in self:
            if not rec.approved_limit:
                raise UserError(_('Enter the reduced approved limit.'))
            rec.write({'state': 'reduced', 'coverage_percent':
                       rec.coverage_percent or
                       rec.policy_id.default_coverage_percent,
                       'decision_date': fields.Date.today()})

    def action_mark_rejected(self):
        self.write({'state': 'rejected',
                    'decision_date': fields.Date.today()})


class SfCiClaim(models.Model):
    _name = 'sf.ci.claim'
    _description = 'Credit Insurance Claim'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Claim Reference', required=True, copy=False,
                       readonly=True, default='New')
    policy_id = fields.Many2one('sf.ci.policy', string='Policy',
                                required=True, ondelete='cascade')
    buyer_id = fields.Many2one('sf.ci.buyer', string='Insured Buyer',
                               required=True,
                               domain="[('policy_id', '=', policy_id)]")
    company_id = fields.Many2one(related='policy_id.company_id', store=True)
    currency_id = fields.Many2one(related='policy_id.currency_id')
    overdue_amount = fields.Monetary(string='Overdue Amount', required=True)
    claimed_amount = fields.Monetary(string='Claimed Amount', required=True)
    indemnity_amount = fields.Monetary(string='Indemnity (computed)',
                                       compute='_compute_indemnity',
                                       store=True)
    waiting_period_days = fields.Integer(string='Waiting Period (days)',
                                         default=180)
    filing_date = fields.Date(string='Filing Date', required=True,
                              default=fields.Date.today)
    settlement_date = fields.Date(string='Settlement Date', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('submitted', 'Submitted'),
        ('accepted', 'Accepted'), ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'), ('rejected', 'Rejected')],
        default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.ci.claim') or 'CIC-NEW'
        return super().create(vals_list)

    @api.depends('claimed_amount', 'buyer_id.coverage_percent')
    def _compute_indemnity(self):
        for rec in self:
            rec.indemnity_amount = rec.claimed_amount * (
                (rec.buyer_id.coverage_percent or 0.0) / 100.0)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_accept(self):
        self.write({'state': 'accepted'})

    def action_mark_paid(self, partial=False):
        for rec in self:
            rec.write({'state': 'partially_paid' if partial else 'paid',
                       'settlement_date': fields.Date.today()})

    def action_reject(self):
        self.write({'state': 'rejected'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.ci.policy'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
