# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CommissionPlan(models.Model):
    _name = 'sf.commission.plan'
    _description = 'Commission Plan'
    _order = 'sequence asc, id asc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Plan Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(string='Active', default=True)
    note = fields.Text(string='Description')

    calculation_type = fields.Selection(
        [
            ('gross', 'Percentage of invoice amount'),
            ('margin', 'Percentage of gross margin'),
        ],
        string='Calculation',
        required=True,
        default='gross',
        help='Commission is computed either on the gross invoice amount '
             'or on the gross margin (amount - cost) of the products.',
    )
    rate = fields.Float(
        string='Rate (%)',
        digits='Commission',
        default=5.0,
        help='Base commission rate in percent.',
    )
    use_tiers = fields.Boolean(
        string='Tiered rates',
        help='Enable progressive rates based on cumulative sales amount.',
    )
    tier_ids = fields.One2many(
        'sf.commission.plan.tier',
        'plan_id',
        string='Tiers',
    )
    rule_ids = fields.One2many(
        'sf.commission.rule',
        'plan_id',
        string='Rules',
        help='Optional overrides per product category or product.',
    )
    min_commission = fields.Monetary(
        string='Minimum Commission',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )
    salesperson_domain = fields.Char(
        string='Salesperson Filter',
        help='Domain for allowed salespeople (empty = all).',
    )
    group_ids = fields.Many2many(
        'res.groups',
        string='Authorized Groups',
        help='If set, only these groups can earn this plan.',
    )

    @api.constrains('rate', 'min_commission')
    def _check_positive(self):
        for plan in self:
            if plan.rate < 0:
                raise ValidationError(_('Commission rate must be positive.'))
            if plan.min_commission < 0:
                raise ValidationError(
                    _('Minimum commission must be positive.'))


class CommissionPlanTier(models.Model):
    _name = 'sf.commission.plan.tier'
    _description = 'Commission Plan Tier'
    _order = 'min_amount asc, id asc'

    plan_id = fields.Many2one(
        'sf.commission.plan',
        string='Plan',
        required=True,
        ondelete='cascade',
    )
    min_amount = fields.Monetary(
        string='From Amount',
        currency_field='currency_id',
        required=True,
    )
    rate = fields.Float(
        string='Rate (%)',
        digits='Commission',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='plan_id.currency_id',
        readonly=True,
    )

    @api.constrains('min_amount', 'rate')
    def _check_tier(self):
        for tier in self:
            if tier.min_amount < 0:
                raise ValidationError(
                    _('Tier minimum amount must be positive.'))
            if tier.rate < 0:
                raise ValidationError(_('Tier rate must be positive.'))


class CommissionRule(models.Model):
    _name = 'sf.commission.rule'
    _description = 'Commission Rule Override'
    _order = 'sequence asc, id asc'

    plan_id = fields.Many2one(
        'sf.commission.plan',
        string='Plan',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=10)
    product_id = fields.Many2one('product.product', string='Product')
    product_category_id = fields.Many2one(
        'product.category',
        string='Product Category',
    )
    rate = fields.Float(
        string='Rate (%)',
        digits='Commission',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='plan_id.currency_id',
        readonly=True,
    )

    @api.constrains('product_id', 'product_category_id')
    def _check_target(self):
        for rule in self:
            if not rule.product_id and not rule.product_category_id:
                raise ValidationError(
                    _('A commission rule must target a product or a '
                      'product category.'))


class CommissionLine(models.Model):
    _name = 'sf.commission.line'
    _description = 'Commission Line'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Reference', required=True, copy=False)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        index=True,
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        required=True,
        tracking=True,
        index=True,
    )
    plan_id = fields.Many2one(
        'sf.commission.plan',
        string='Commission Plan',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Source Order',
        readonly=True,
        states={'draft': [('readonly', False)]},
        ondelete='set null',
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Source Invoice',
        readonly=True,
        states={'draft': [('readonly', False)]},
        ondelete='set null',
    )
    base_amount = fields.Monetary(
        string='Base Amount',
        currency_field='currency_id',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Amount on which the commission is computed '
             '(invoice total or margin).',
    )
    rate = fields.Float(
        string='Rate (%)',
        digits='Commission',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    commission = fields.Monetary(
        string='Commission',
        currency_field='currency_id',
        compute='_compute_commission',
        store=True,
        readonly=False,
        tracking=True,
    )
    adjustment = fields.Monetary(
        string='Adjustment',
        currency_field='currency_id',
        default=0.0,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Positive or negative manual adjustment.',
    )
    final_commission = fields.Monetary(
        string='Final Commission',
        currency_field='currency_id',
        compute='_compute_final_commission',
        store=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    note = fields.Text(string='Notes')

    @api.depends('base_amount', 'rate', 'plan_id.min_commission')
    def _compute_commission(self):
        for line in self:
            commission = 0.0
            if line.base_amount:
                commission = line.base_amount * line.rate / 100.0
            if line.plan_id and line.plan_id.min_commission:
                commission = max(commission, line.plan_id.min_commission)
            line.commission = commission

    @api.depends('commission', 'adjustment')
    def _compute_final_commission(self):
        for line in self:
            line.final_commission = line.commission + line.adjustment

    @api.onchange('salesperson_id', 'sale_order_id')
    def _onchange_order(self):
        if self.sale_order_id and not self.salesperson_id:
            self.salesperson_id = self.sale_order_id.user_id.id

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_paid(self):
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})