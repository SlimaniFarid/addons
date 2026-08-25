# -*- coding: utf-8 -*-
"""Supplier Performance Review Meeting models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_performance_review(models.Model):
    _name = 'sf.supplier_performance_review'
    _description = 'Supplier Performance Review Meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    review_date = fields.Date(string='Review Date', required=True, default=fields.Date.today)
    overall_score = fields.Float(string='Overall Score')
    improvement_areas = fields.Html(string='Improvement Areas')
    commitments = fields.Text(string='Supplier Commitments')
    next_review = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier_performance_review') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

