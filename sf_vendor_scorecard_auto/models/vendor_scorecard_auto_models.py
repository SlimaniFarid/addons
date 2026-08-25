# -*- coding: utf-8 -*-
"""Automated Vendor Scorecard models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVendor_scorecard_auto(models.Model):
    _name = 'sf.vendor_scorecard_auto'
    _description = 'Automated Vendor Scorecard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    otd_percent = fields.Float(string='On-Time Delivery %')
    quality_percent = fields.Float(string='Quality Acceptance %')
    invoice_accuracy = fields.Float(string='Invoice Accuracy %')
    overall_score = fields.Float(string='Overall Score')
    trend = fields.Selection([
        ('up', 'Improving'),
        ('stable', 'Stable'),
        ('down', 'Declining'),
        ], string='Trend', default=stable)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.vendor_scorecard_auto') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

