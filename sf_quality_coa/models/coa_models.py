# -*- coding: utf-8 -*-
"""Certificate of Analysis models."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCoa(models.Model):
    _name = 'sf.coa'
    _description = 'Certificate of Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='CoA Number', required=True, copy=False,
                       readonly=True, default='New')
    picking_id = fields.Many2one('stock.picking', string='Delivery',
                                 required=True,
                                 domain=[('picking_type_id.code', '=',
                                          'outgoing')])
    partner_id = fields.Many2one(related='picking_id.partner_id',
                                 string='Customer', store=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial')
    production_date = fields.Date(string='Production Date')
    expiry_date = fields.Date(string='Expiry Date')
    line_ids = fields.One2many('sf.coa.line', 'coa_id',
                               string='Test Parameters')
    passed_all = fields.Boolean(string='All Parameters Passed',
                                compute='_compute_verdict', store=True)
    tested_by_id = fields.Many2one('res.users', string='Tested By',
                                   readonly=True)
    approved_by_id = fields.Many2one('res.users', string='Approved By',
                                     readonly=True)
    approved_date = fields.Date(readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('tested', 'Tested'), ('approved', 'Approved'),
        ('issued', 'Issued'), ('rejected', 'Rejected')],
        default='draft', tracking=True, copy=False)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.coa') or 'COA-NEW'
        return super().create(vals_list)

    @api.depends('line_ids.verdict')
    def _compute_verdict(self):
        for rec in self:
            rec.passed_all = bool(rec.line_ids) and all(
                l.verdict == 'pass' for l in rec.line_ids)

    @api.onchange('picking_id')
    def _onchange_picking(self):
        if self.picking_id:
            moves = self.picking_id.move_ids
            if moves:
                self.product_id = moves[0].product_id
                lines = moves[0].move_line_ids
                if lines:
                    self.lot_id = lines[0].lot_id

    def action_mark_tested(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Enter test results first.'))
        self.write({'state': 'tested', 'tested_by_id': self.env.uid})

    def action_approve(self):
        self.ensure_one()
        if not self.passed_all:
            raise UserError(_('Some parameters failed - CoA cannot be '
                              'approved.'))
        self.write({'state': 'approved', 'approved_by_id': self.env.uid,
                    'approved_date': fields.Date.today()})

    def action_issue(self):
        self.write({'state': 'issued'})

    def action_reject(self):
        self.write({'state': 'rejected'})


class SfCoaLine(models.Model):
    _name = 'sf.coa.line'
    _description = 'CoA Test Parameter'

    coa_id = fields.Many2one('sf.coa', string='CoA', required=True,
                             ondelete='cascade')
    company_id = fields.Many2one(related='coa_id.company_id', store=True)
    sequence = fields.Integer(default=10)
    parameter = fields.Char(string='Test Parameter', required=True)
    specification = fields.Char(string='Specification / Acceptance Criteria')
    result_value = fields.Char(string='Measured Result')
    unit = fields.Char(string='Unit')
    test_method = fields.Char(string='Test Method')
    verdict = fields.Selection([
        ('pass', 'Pass'), ('fail', 'Fail'), ('pending', 'Pending')],
        default='pending', string='Verdict')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.coa'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
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

