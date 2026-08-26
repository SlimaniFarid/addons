# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LitigationCase(models.Model):
    _name = 'sf.litigation.case'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Litigation Case'
    _order = 'id desc'

    name = fields.Char(string='Case Number', required=True, index=True,
                       tracking=True)
    case_type = fields.Selection([
        ('commercial', 'Commercial'),
        ('social', 'Social'),
        ('fiscal', 'Fiscal'),
        ('civil', 'Civil'),
        ('criminal', 'Criminal'),
        ('other', 'Other'),
    ], string='Legal domain', required=True, tracking=True, index=True)
    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    plaintiff_id = fields.Many2one('res.partner', string='Plaintiff',
                                   ondelete='restrict')
    defendant_id = fields.Many2one('res.partner', string='Defendant',
                                   ondelete='restrict')
    third_party_ids = fields.Many2many('res.partner',
                                       string='Third parties')
    lawyer_id = fields.Many2one('res.partner', string='Lawyer',
                                ondelete='restrict')
    court = fields.Char(string='Court')
    jurisdiction = fields.Char(string='Jurisdiction')
    claim_amount = fields.Float(string='Claim amount')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('opened', 'Opened'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    opened_date = fields.Date(string='Opened date')
    closed_date = fields.Date(string='Closed date')
    closed_reason = fields.Text(string='Closing reason')
    deadline_ids = fields.One2many('sf.litigation.deadline', 'case_id',
                                   string='Procedural deadlines')
    fee_ids = fields.One2many('sf.litigation.fee', 'case_id', string='Fees')
    decision_ids = fields.One2many('sf.litigation.decision', 'case_id',
                                   string='Decisions')
    total_fees = fields.Float(string='Total fees',
                              compute='_compute_total_fees', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('fee_ids.amount')
    def _compute_total_fees(self):
        for case in self:
            case.total_fees = sum(case.fee_ids.mapped('amount'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.litigation.case')
            vals['name'] = 'LIT-%s' % seq
        return super().create(vals)

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft cases can be opened.'))
        self.write({'state': 'opened',
                    'opened_date': fields.Date.today()})

    def action_pending(self):
        self.ensure_one()
        if self.state != 'opened':
            raise UserError(_('Only opened cases can be marked pending.'))
        self.state = 'pending'

    def action_close(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_litigation.group_litigation_manager'):
            raise UserError(_('Only litigation managers can close cases.'))
        if self.state != 'pending':
            raise UserError(_('Only pending cases can be closed.'))
        recorded = self.decision_ids.filtered(
            lambda d: d.state == 'recorded')
        if not recorded and not self.closed_reason:
            raise UserError(_('A case cannot be closed without a recorded '
                              'decision or a closing reason.'))
        self.write({'state': 'closed',
                    'closed_date': fields.Date.today()})