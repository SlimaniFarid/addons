# -*- coding: utf-8 -*-
"""Transfer pricing policies, transaction analysis and documentation."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfTpPolicy(models.Model):
    """Arm-length pricing policy between two entities of the group."""
    _name = 'sf.tp.policy'
    _description = 'Transfer Pricing Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'valid_from desc'

    name = fields.Char(string='Policy Reference', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Selling Entity',
                                 required=True, default=lambda s: s.env.company)
    counterpart_company_id = fields.Many2one(
        'res.company', string='Buying Entity', required=True,
        domain=[('id', '!=', company_id)])
    ic_partner_id = fields.Many2one(
        'res.partner', string='IC Partner of Buying Entity',
        required=True,
        help='Partner record used on invoices from the selling entity to '
             'the buying entity.')
    method = fields.Selection([
        ('cup', 'CUP - Comparable Uncontrolled Price'),
        ('cost_plus', 'Cost Plus'),
        ('resale_minus', 'Resale Minus'),
        ('tnmm', 'TNMM - Transactional Net Margin'),
    ], string='Method', required=True, default='cost_plus')
    markup_percent = fields.Float(
        string='Markup %', help='Cost-plus / TNMM operating margin markup.')
    target_margin_percent = fields.Float(
        string='Target Resale Margin %', help='Resale-minus target margin.')
    valid_from = fields.Date(string='Valid From', required=True,
                             default=fields.Date.today)
    valid_to = fields.Date(string='Valid To')
    review_threshold_percent = fields.Float(
        string='Review Threshold %', default=5.0,
        help='Variance beyond this % requires documented review.')
    documentation_ref = fields.Char(string='Documentation Reference')
    apa_ref = fields.Char(string='APA Reference')
    state = fields.Selection([
        ('draft', 'Draft'), ('active', 'Active'), ('expired', 'Expired')],
        default='draft', tracking=True)
    notes = fields.Html(string='Method Notes / Benchmarking')
    company_id_in_rule = fields.Boolean()
    transaction_ids = fields.One2many('sf.tp.transaction', 'policy_id',
                                      string='Analysed Transactions')
    transaction_count = fields.Integer(compute='_compute_counts')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.tp.policy') or 'TPP-NEW'
        return super().create(vals_list)

    def _compute_counts(self):
        for rec in self:
            rec.transaction_count = len(rec.transaction_ids)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_expire(self):
        self.write({'state': 'expired'})

    def _compute_alp(self, cost, resale_price):
        """Arm's length unit price under the policy method."""
        self.ensure_one()
        if self.method == 'cost_plus':
            return cost * (1.0 + self.markup_percent / 100.0)
        if self.method == 'resale_minus':
            return resale_price * (1.0 - self.target_margin_percent / 100.0)
        if self.method == 'tnmm':
            return cost * (1.0 + self.markup_percent / 100.0)
        return 0.0  # CUP: external benchmark entered manually


class SfTpTransaction(models.Model):
    """One intercompany invoice line analysed against the policy."""
    _name = 'sf.tp.transaction'
    _description = 'TP Transaction Analysis'
    _order = 'invoice_date desc, id desc'

    policy_id = fields.Many2one('sf.tp.policy', string='Policy', required=True,
                                ondelete='cascade')
    company_id = fields.Many2one(related='policy_id.company_id', store=True)
    currency_id = fields.Many2one(related='policy_id.company_id.currency_id')
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    invoice_date = fields.Date(string='Invoice Date')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Qty')
    actual_unit_price = fields.Float(string='Actual Unit Price')
    cost_base = fields.Float(string='Cost Base (unit)')
    resale_price = fields.Float(string='Resale Price (unit)')
    computed_alp = fields.Float(string="Arm's Length Price", readonly=True)
    variance = fields.Float(string='Variance', compute='_compute_variance',
                            store=True)
    variance_percent = fields.Float(string='Variance %',
                                    compute='_compute_variance', store=True)
    review_required = fields.Boolean(string='Review Required',
                                     compute='_compute_review', store=True)
    reviewed_by_id = fields.Many2one('res.users', string='Reviewed By')
    review_notes = fields.Text(string='Review Notes')
    state = fields.Selection([
        ('computed', 'Computed'), ('reviewed', 'Reviewed')],
        default='computed', tracking=True)

    @api.depends('actual_unit_price', 'computed_alp')
    def _compute_variance(self):
        for rec in self:
            rec.variance = rec.actual_unit_price - rec.computed_alp
            rec.variance_percent = (
                (rec.variance / rec.computed_alp * 100.0)
                if rec.computed_alp else 0.0)

    @api.depends('variance_percent', 'policy_id.review_threshold_percent')
    def _compute_review(self):
        for rec in self:
            rec.review_required = abs(rec.variance_percent) > (
                rec.policy_id.review_threshold_percent or 0.0)

    def action_mark_reviewed(self):
        for rec in self:
            rec.write({'state': 'reviewed', 'reviewed_by_id': rec.env.uid})


class SfTpDocumentation(models.Model):
    """Master File / Local File register per fiscal year."""
    _name = 'sf.tp.documentation'
    _description = 'TP Documentation (Master / Local File)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True)
    doc_type = fields.Selection([
        ('master_file', 'Master File'),
        ('local_file', 'Local File'),
        ('cbcr_ref', 'CbCR Reference')],
        required=True, default='local_file')
    fiscal_year = fields.Char(string='Fiscal Year', required=True)
    entity_scope = fields.Many2many('res.company', string='Entities Covered')
    owner_id = fields.Many2one('res.users', string='Documentation Owner')
    state = fields.Selection([
        ('draft', 'Draft'), ('in_review', 'In Review'), ('final', 'Final')],
        default='draft', tracking=True)
    review_date = fields.Date(string='Next Review Date')
    content = fields.Html(string='Content / Sections')
    attachment_ids = fields.Many2many('ir.attachment',
                                      string='Supporting Files')
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    def action_set_in_review(self):
        self.write({'state': 'in_review'})

    def action_set_final(self):
        self.write({'state': 'final'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.tp.policy'

    active = fields.Boolean(string='Active', default=True)
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('review_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.review_date
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

