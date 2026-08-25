# -*- coding: utf-8 -*-
"""CAPEX request and approval models."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCapexRequest(models.Model):
    _name = 'sf.capex.request'
    _description = 'CAPEX Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Request Reference', required=True, copy=False,
                       readonly=True, default='New')
    title = fields.Char(string='Title', required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    requester_id = fields.Many2one('res.users', string='Requested By',
                                   default=lambda s: s.env.uid)
    department = fields.Selection([
        ('production', 'Production'), ('logistics', 'Logistics'),
        ('it', 'IT'), ('facilities', 'Facilities'),
        ('r_and_d', 'R&D'), ('commercial', 'Commercial'),
        ('other', 'Other')], required=True, default='production')
    category = fields.Selection([
        ('equipment', 'Equipment / Machinery'),
        ('vehicle', 'Vehicle / Fleet'),
        ('building', 'Building / Infrastructure'),
        ('it_hardware', 'IT Hardware'),
        ('software', 'Software / Licenses'),
        ('r_and_d', 'R&D / Innovation'),
        ('other', 'Other')], required=True, default='equipment')
    description = fields.Html(string='Business Case')
    requested_amount = fields.Monetary(string='Requested Amount', required=True)
    approved_amount = fields.Monetary(string='Approved Amount')
    expected_date = fields.Date(string='Expected Purchase Date')
    useful_life_years = fields.Integer(string='Useful Life (years)', default=5)
    annual_benefit = fields.Monetary(string='Expected Annual Benefit')
    payback_years = fields.Float(string='Payback (years)',
                                 compute='_compute_payback', store=True)
    vendor_suggestion_id = fields.Many2one('res.partner',
                                           string='Suggested Vendor')
    po_reference = fields.Char(string='PO Reference')
    asset_reference = fields.Char(string='Asset Reference',
                                  help='Fixed asset code once capitalized.')
    approval_ids = fields.One2many('sf.capex.approval', 'request_id',
                                   string='Approval Chain', copy=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('submitted', 'Submitted'),
        ('approved', 'Approved'), ('rejected', 'Rejected'),
        ('ordered', 'Ordered'), ('capitalized', 'Capitalized'),
        ('cancelled', 'Cancelled')], default='draft', tracking=True,
        copy=False)
    submitted_date = fields.Date(readonly=True)
    approved_date = fields.Date(readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.capex.request') or 'CAPEX-NEW'
        return super().create(vals_list)

    @api.depends('requested_amount', 'annual_benefit')
    def _compute_payback(self):
        for rec in self:
            rec.payback_years = (rec.requested_amount / rec.annual_benefit
                                 if rec.annual_benefit else 0.0)

    def action_submit(self):
        self.ensure_one()
        if not self.approval_ids:
            raise UserError(
                _('Add at least one approval level before submitting.'))
        self.write({'state': 'submitted',
                    'submitted_date': fields.Date.today()})

    def _all_approved(self):
        return all(a.state == 'approved' for a in self.approval_ids)

    def _check_and_approve(self):
        self.ensure_one()
        if self._all_approved():
            self.write({'state': 'approved',
                        'approved_date': fields.Date.today()})

    def action_approve_level(self):
        self.ensure_one()
        pending = self.approval_ids.filtered(lambda a: a.state == 'pending')
        if not pending:
            raise UserError(_('No pending approval level.'))
        pending[0].write({'state': 'approved',
                          'approver_user_id': self.env.uid,
                          'approval_date': fields.Date.today()})
        self._check_and_approve()

    def action_reject(self):
        self.ensure_one()
        self.approval_ids.filtered(
            lambda a: a.state == 'pending').write({'state': 'rejected'})
        self.write({'state': 'rejected'})

    def action_mark_ordered(self):
        self.ensure_one()
        if self.state != 'approved':
            raise UserError(_('Only approved requests can be ordered.'))
        self.write({'state': 'ordered'})

    def action_capitalize(self):
        self.ensure_one()
        if self.state != 'ordered':
            raise UserError(_('Mark the request as Ordered first.'))
        if not self.asset_reference:
            raise UserError(_('Enter the fixed asset reference.'))
        self.write({'state': 'capitalized'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class SfCapexApproval(models.Model):
    _name = 'sf.capex.approval'
    _description = 'CAPEX Approval Level'
    _order = 'sequence, id'

    request_id = fields.Many2one('sf.capex.request', required=True,
                                 ondelete='cascade')
    sequence = fields.Integer(default=10)
    role_name = fields.Char(string='Level', required=True,
                            help='e.g. Department Head, CFO, GM')
    required_amount_from = fields.Float(string='Required From Amount')
    required_amount_to = fields.Float(string='Required To Amount (0 = no limit)')
    approver_user_id = fields.Many2one('res.users', string='Approved By',
                                       readonly=True)
    approval_date = fields.Date(readonly=True)
    comment = fields.Text(string='Comment')
    state = fields.Selection([
        ('pending', 'Pending'), ('approved', 'Approved'),
        ('rejected', 'Rejected')], default='pending', tracking=True)
    currency_id = fields.Many2one(related='request_id.currency_id')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.capex.request'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
