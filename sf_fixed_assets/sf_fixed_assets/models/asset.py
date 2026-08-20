# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Asset(models.Model):
    _name = 'sf.fixed.asset'
    _description = 'Fixed Asset'
    _rec_name = 'name'
    _order = 'purchase_date desc'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, size=20)
    category_id = fields.Many2one(
        'sf.fixed.asset.category', string='Category', required=True)
    location = fields.Char(string='Location')
    owner_id = fields.Many2one('res.partner', string='Owner')
    purchase_date = fields.Date(string='Purchase Date', required=True)
    purchase_value = fields.Monetary(string='Purchase Value', required=True)
    residual_value = fields.Monetary(
        string='Residual Value', default=0.0,
        help="Value remaining at the end of useful life.")
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_use', 'In Use'),
        ('disposed', 'Disposed'),
        ('sold', 'Sold'),
    ], string='Status', default='draft', tracking=True)
    useful_life_months = fields.Integer(
        string='Useful Life (months)',
        compute='_compute_category_fields', store=True, readonly=False)
    depreciation_method = fields.Selection(
        [('straight_line', 'Straight Line'),
         ('declining', 'Declining Balance')],
        string='Depreciation Method',
        compute='_compute_category_fields', store=True, readonly=False)
    monthly_depreciation = fields.Monetary(
        string='Monthly Depreciation', compute='_compute_depreciation',
        store=True)
    accumulated_depreciation = fields.Monetary(
        string='Accumulated Depreciation', compute='_compute_depreciation',
        store=True)
    book_value = fields.Monetary(
        string='Book Value', compute='_compute_depreciation', store=True)
    depreciation_ids = fields.One2many(
        'sf.fixed.asset.depreciation', 'asset_id',
        string='Depreciation Lines')
    note = fields.Text(string='Note')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)

    @api.depends('category_id')
    def _compute_category_fields(self):
        for asset in self:
            asset.useful_life_months = (
                asset.category_id.useful_life_months or 60)
            asset.depreciation_method = (
                asset.category_id.depreciation_method or 'straight_line')

    @api.depends('purchase_value', 'residual_value', 'useful_life_months',
                 'depreciation_ids.amount')
    def _compute_depreciation(self):
        for asset in self:
            if asset.useful_life_months:
                depreciable = asset.purchase_value - asset.residual_value
                asset.monthly_depreciation = round(
                    depreciable / asset.useful_life_months, 2)
            else:
                asset.monthly_depreciation = 0.0
            asset.accumulated_depreciation = sum(
                asset.depreciation_ids.mapped('amount') or [0.0])
            asset.book_value = max(
                asset.purchase_value - asset.accumulated_depreciation,
                asset.residual_value)

    def action_generate_depreciation(self):
        """Generate the full depreciation plan for this asset."""
        self.ensure_one()
        if self.depreciation_ids:
            self.depreciation_ids.unlink()
        plan = []
        remaining = self.purchase_value - self.residual_value
        for month in range(self.useful_life_months):
            amount = self.monthly_depreciation if month < self.useful_life_months - 1 \
                else round(remaining, 2)
            remaining -= amount
            plan.append((0, 0, {
                'asset_id': self.id,
                'period': month + 1,
                'amount': amount,
            }))
        self.depreciation_ids = plan
        return True

    def action_in_use(self):
        self.write({'state': 'in_use'})

    def action_dispose(self):
        self.write({'state': 'disposed'})

    def action_sold(self):
        self.write({'state': 'sold'})