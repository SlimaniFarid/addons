# -*- coding: utf-8 -*-
"""Change request and CAB models."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfChangeRequest(models.Model):
    _name = 'sf.change.request'
    _description = 'Change Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Change Reference', required=True, copy=False,
                       readonly=True, default='New')
    title = fields.Char(string='Title', required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    requester_id = fields.Many2one('res.users', string='Requested By',
                                   default=lambda s: s.env.uid)
    change_type = fields.Selection([
        ('it', 'IT / System'), ('process', 'Process'),
        ('product', 'Product / Design'), ('facility', 'Facility'),
        ('supplier', 'Supplier Change')], required=True, default='it')
    risk_level = fields.Selection([
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        required=True, default='medium', tracking=True)
    description = fields.Html(string='Change Description')
    impact_analysis = fields.Html(string='Impact Analysis')
    implementation_plan = fields.Html(string='Implementation Plan')
    rollback_plan = fields.Html(string='Rollback Plan', required=True)
    planned_date = fields.Datetime(string='Planned Implementation')
    cab_date = fields.Datetime(string='CAB Meeting Date')
    implementer_id = fields.Many2one('res.users', string='Implementer')
    vote_ids = fields.One2many('sf.change.vote', 'request_id',
                               string='CAB Votes')
    approval_percent = fields.Float(string='Approval %',
                                    compute='_compute_votes', store=True)
    post_impl_review = fields.Html(string='Post-Implementation Review')
    state = fields.Selection([
        ('draft', 'Draft'), ('submitted', 'Submitted'),
        ('cab_review', 'CAB Review'), ('approved', 'Approved'),
        ('implemented', 'Implemented'), ('closed', 'Closed'),
        ('failed', 'Failed'), ('rejected', 'Rejected')],
        default='draft', tracking=True, copy=False)
    implemented_at = fields.Datetime(readonly=True)
    closed_at = fields.Datetime(readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.change.request') or 'CHG-NEW'
        return super().create(vals_list)

    @api.depends('vote_ids.vote')
    def _compute_votes(self):
        for rec in self:
            votes = rec.vote_ids
            rec.approval_percent = (len(votes.filtered(
                lambda v: v.vote == 'approve')) / len(votes) * 100.0
                if votes else 0.0)

    def action_submit(self):
        self.ensure_one()
        if not self.rollback_plan:
            raise UserError(_('A rollback plan is mandatory.'))
        self.write({'state': 'submitted'})

    def action_open_cab(self):
        self.ensure_one()
        if not self.vote_ids:
            raise UserError(_('Add CAB members before opening the review.'))
        self.write({'state': 'cab_review'})

    def action_close_cab(self):
        self.ensure_one()
        if self.approval_percent < 50.0:
            self.write({'state': 'rejected'})
        else:
            self.write({'state': 'approved'})

    def action_implemented(self):
        self.write({'state': 'implemented',
                    'implemented_at': fields.Datetime.now()})

    def action_close(self):
        self.write({'state': 'closed', 'closed_at': fields.Datetime.now()})

    def action_failed(self):
        self.write({'state': 'failed'})


class SfChangeVote(models.Model):
    _name = 'sf.change.vote'
    _description = 'CAB Vote'

    request_id = fields.Many2one('sf.change.request', string='Change',
                                 required=True, ondelete='cascade')
    company_id = fields.Many2one(related='request_id.company_id', store=True)
    member_id = fields.Many2one('res.users', string='CAB Member',
                                required=True)
    vote = fields.Selection([
        ('approve', 'Approve'), ('reject', 'Reject'),
        ('abstain', 'Abstain')], default='approve')
    comment = fields.Text(string='Comment')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.change.request'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
