# -*- coding: utf-8 -*-
"""Customer contract renewal management."""
import dateutil.relativedelta as rd

from odoo import api, fields, models, _


class SfRenewalContract(models.Model):
    _name = 'sf.renewal.contract'
    _description = 'Customer Contract for Renewal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'end_date asc'

    name = fields.Char(string='Contract Reference', required=True, copy=False,
                       readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True, tracking=True,
                                 domain=[('customer_rank', '>', 0)])
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    contract_type = fields.Selection([
        ('service', 'Service Agreement'),
        ('maintenance', 'Maintenance'),
        ('subscription', 'Subscription'),
        ('rental', 'Rental / Leasing'),
        ('supply', 'Supply Agreement'),
        ('other', 'Other')], required=True, default='service')
    owner_id = fields.Many2one('res.users', string='Account Owner',
                               default=lambda s: s.env.uid)
    start_date = fields.Date(string='Start Date', required=True,
                             default=fields.Date.today)
    end_date = fields.Date(string='End Date (current term)', required=True)
    notice_period_days = fields.Integer(string='Notice Period (days)',
                                        default=30,
                                        help='Days before end date by which '
                                             'notice must be given.')
    auto_renew = fields.Boolean(string='Auto-Renewal Clause')
    annual_value = fields.Monetary(string='Annual Contract Value')
    renewal_value = fields.Monetary(string='Proposed Renewal Value')
    churn_risk = fields.Selection([
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='low', tracking=True)
    next_action_date = fields.Date(string='Next Action Date')
    next_action_note = fields.Char(string='Next Action')
    notice_deadline = fields.Date(string='Notice Deadline',
                                  compute='_compute_deadlines', store=True)
    days_to_notice = fields.Integer(string='Days to Notice',
                                    compute='_compute_deadlines', store=True)
    days_to_expiry = fields.Integer(string='Days to Expiry',
                                    compute='_compute_deadlines', store=True)
    expiring_soon = fields.Boolean(compute='_compute_deadlines', store=True)
    state = fields.Selection([
        ('active', 'Active'), ('expiring', 'Expiring Soon'),
        ('renewed', 'Renewed'), ('lost', 'Lost'), ('expired', 'Expired')],
        default='active', tracking=True)
    renewed_end_date = fields.Date(string='Renewed Until', readonly=True)
    lost_reason = fields.Text(string='Lost Reason')
    company_id_in_rule = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.renewal.contract') or 'REN-NEW'
        return super().create(vals_list)

    @api.depends('end_date', 'notice_period_days')
    def _compute_deadlines(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.end_date:
                rec.notice_deadline = rec.end_date - rd.relativedelta(
                    days=rec.notice_period_days)
                rec.days_to_notice = (rec.notice_deadline - today).days
                rec.days_to_expiry = (rec.end_date - today).days
                rec.expiring_soon = rec.days_to_notice <= 0 and \
                    rec.days_to_expiry >= 0
            else:
                rec.notice_deadline = False
                rec.days_to_notice = 0
                rec.days_to_expiry = 0
                rec.expiring_soon = False

    def action_flag_expiring(self):
        for rec in self:
            if rec.expiring_soon and rec.state == 'active':
                rec.write({'state': 'expiring'})

    def action_mark_renewed(self):
        self.ensure_one()
        if not self.renewed_end_date:
            self.renewed_end_date = self.end_date + rd.relativedelta(years=1)
        self.write({'end_date': self.renewed_end_date, 'state': 'active'})

    def action_mark_lost(self):
        self.write({'state': 'lost'})

    def action_mark_expired(self):
        self.write({'state': 'expired'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.renewal.contract'

    active = fields.Boolean(string='Active', default=True)
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
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

