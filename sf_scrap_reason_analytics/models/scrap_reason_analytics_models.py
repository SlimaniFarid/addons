# -*- coding: utf-8 -*-
"""Scrap Reason Analytics models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfScrapReason(models.Model):
    _name = 'sf.scrap.reason'
    _description = 'Scrap Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order')
    product_id = fields.Many2one('product.product', string='Product Scrapped', required=True)
    quantity = fields.Float(string='Qty Scrapped')
    reason_code = fields.Selection([
        ('setup', 'Setup Scrap'),
        ('defect', 'Defect'),
        ('material', 'Material Defect'),
        ('machine', 'Machine Fault'),
        ('operator', 'Operator Error'),
        ('other', 'Other'),
        ], string='Reason Code', required=True)
    cost = fields.Monetary(string='Scrap Cost')
    action_ref = fields.Char(string='Improvement Action Ref')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('analyzed', 'Analyzed'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.scrap.reason') or 'NEW'
        return super().create(vals_list)

    def action_analyzed(self):
        self.write({'state': 'analyzed'})

    def action_closed(self):
        self.write({'state': 'closed'})

