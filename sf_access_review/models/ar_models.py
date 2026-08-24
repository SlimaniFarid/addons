# -*- coding: utf-8 -*-
"""Access recertification campaigns."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAccessCampaign(models.Model):
    _name = 'sf.access.campaign'
    _description = 'Access Review Campaign'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'due_date desc'

    name = fields.Char(string='Campaign', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    scope = fields.Selection([
        ('all', 'All Users'), ('admins', 'Admin / Privileged Only')],
        required=True, default='all')
    reviewer_id = fields.Many2one('res.users', string='Lead Reviewer')
    due_date = fields.Date(string='Due Date', required=True)
    line_ids = fields.One2many('sf.access.review', 'campaign_id',
                               string='Review Lines')
    user_count = fields.Integer(compute='_compute_stats')
    reviewed_count = fields.Integer(compute='_compute_stats')
    revoke_count = fields.Integer(compute='_compute_stats')
    state = fields.Selection([
        ('draft', 'Draft'), ('open', 'Open'), ('closed', 'Closed')],
        default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.access.campaign') or 'ACC-NEW'
        return super().create(vals_list)

    def _compute_stats(self):
        for rec in self:
            rec.user_count = len(rec.line_ids)
            rec.reviewed_count = len(rec.line_ids.filtered(
                lambda l: l.decision != 'pending'))
            rec.revoke_count = len(rec.line_ids.filtered(
                lambda l: l.decision == 'revoke'))

    def action_open(self):
        self.ensure_one()
        if self.line_ids:
            raise UserError(_('Review lines already generated.'))
        domain = [('share', '=', False),
                  ('company_ids', 'in', [self.company_id.id])]
        if self.scope == 'admins':
            domain.append(('groups_id', 'in',
                           [self.env.ref('base.group_system').id]))
        users = self.env['res.users'].search(domain)
        vals_list = []
        for user in users:
            groups = ', '.join(user.groups_id.mapped('name'))[:400]
            vals_list.append({
                'campaign_id': self.id, 'user_id': user.id,
                'groups_summary': groups})
        if vals_list:
            self.env['sf.access.review'].create(vals_list)
        self.write({'state': 'open'})

    def action_close(self):
        self.ensure_one()
        pending = self.line_ids.filtered(
            lambda l: l.decision == 'pending')
        if pending:
            raise UserError(_('%s reviews are still pending.')
                            % len(pending))
        self.write({'state': 'closed'})


class SfAccessReview(models.Model):
    _name = 'sf.access.review'
    _description = 'Access Review Line'

    campaign_id = fields.Many2one('sf.access.campaign', string='Campaign',
                                  required=True, ondelete='cascade')
    company_id = fields.Many2one(related='campaign_id.company_id', store=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    groups_summary = fields.Char(string='Current Groups', readonly=True)
    decision = fields.Selection([
        ('pending', 'Pending'), ('keep', 'Keep'), ('revoke', 'Revoke')],
        default='pending', tracking=True)
    reviewer_id = fields.Many2one('res.users', string='Reviewed By',
                                  readonly=True)
    review_date = fields.Date(readonly=True)
    comments = fields.Text(string='Comments')

    def action_keep(self):
        for rec in self:
            rec.write({'decision': 'keep',
                       'reviewer_id': rec.env.uid,
                       'review_date': fields.Date.today()})

    def action_revoke(self):
        for rec in self:
            rec.write({'decision': 'revoke',
                       'reviewer_id': rec.env.uid,
                       'review_date': fields.Date.today()})
