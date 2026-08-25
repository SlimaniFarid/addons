# -*- coding: utf-8 -*-
"""KYC/AML due diligence files."""
import dateutil.relativedelta as rd

from odoo import api, fields, models, _


class SfKycFile(models.Model):
    _name = 'sf.kyc.file'
    _description = 'KYC File'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'next_review_date asc'

    name = fields.Char(string='KYC Reference', required=True, copy=False,
                       readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer / Partner',
                                 required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    file_type = fields.Selection([
        ('customer', 'Customer KYC'), ('vendor', 'Vendor KYC'),
        ('ubo', 'UBO Declaration')], required=True, default='customer')
    risk_rating = fields.Selection([
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='low', required=True, tracking=True)
    state = fields.Selection([
        ('pending', 'Pending'), ('approved', 'Approved'),
        ('rejected', 'Rejected'), ('expired', 'Expired')],
        default='pending', tracking=True)
    screening_date = fields.Date(string='Last PEP/Sanctions Screening')
    screening_result = fields.Selection([
        ('clear', 'Clear'), ('match', 'Potential Match'),
        ('pending', 'Pending')], default='pending', string='Screening Result')
    ubo_declared = fields.Boolean(string='UBO Declared')
    id_document = fields.Boolean(string='ID Document Received')
    proof_of_address = fields.Boolean(string='Proof of Address Received')
    bank_statement = fields.Boolean(string='Bank Details Verified')
    review_frequency_months = fields.Integer(string='Review Cycle (months)',
                                             default=12)
    last_review_date = fields.Date(string='Last Review')
    next_review_date = fields.Date(string='Next Review',
                                   compute='_compute_next_review', store=True)
    review_overdue = fields.Boolean(compute='_compute_next_review',
                                    store=True)
    reviewer_id = fields.Many2one('res.users', string='Compliance Reviewer')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.kyc.file') or 'KYC-NEW'
        return super().create(vals_list)

    @api.depends('last_review_date', 'review_frequency_months', 'state')
    def _compute_next_review(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.last_review_date and rec.review_frequency_months:
                rec.next_review_date = rec.last_review_date + rd.relativedelta(
                    months=rec.review_frequency_months)
                rec.review_overdue = (rec.next_review_date < today
                                      and rec.state == 'approved')
            else:
                rec.next_review_date = False
                rec.review_overdue = False

    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved',
                       'last_review_date': fields.Date.context_today(rec)})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_expire(self):
        self.write({'state': 'expired'})

    def action_run_screening(self):
        for rec in self:
            rec.screening_date = fields.Date.context_today(rec)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.kyc.file'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('last_review_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.last_review_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

