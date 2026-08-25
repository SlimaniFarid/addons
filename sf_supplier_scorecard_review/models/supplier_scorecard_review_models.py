# -*- coding: utf-8 -*-
"""Supplier Scorecard Review Meetings models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierReview(models.Model):
    _name = 'sf.supplier.review'
    _description = 'Supplier Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    review_date = fields.Date(string='Review Date', required=True, default=fields.Date.today)
    quality_score = fields.Float(string='Quality Score')
    delivery_score = fields.Float(string='Delivery Score')
    actions = fields.Html(string='Improvement Actions')
    next_review = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('held', 'Held'),
        ('actions_tracked', 'Actions Tracked'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.review') or 'NEW'
        return super().create(vals_list)

    def action_held(self):
        self.write({'state': 'held'})

    def action_actions_tracked(self):
        self.write({'state': 'actions_tracked'})

