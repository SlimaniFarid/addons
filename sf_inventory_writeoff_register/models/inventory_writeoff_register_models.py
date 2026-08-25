# -*- coding: utf-8 -*-
"""Inventory Write-Off Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfWriteoff(models.Model):
    _name = 'sf.writeoff'
    _description = 'Write-Off'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity')
    value = fields.Monetary(string='Value', required=True)
    reason = fields.Selection([
        ('expiry', 'Expiry'),
        ('damage', 'Damage'),
        ('theft', 'Theft'),
        ('obsolete', 'Obsolete'),
        ('count', 'Count Correction'),
        ], string='Reason', required=True)
    approved_by_id = fields.Many2one('res.users', string='Approved By')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('proposed', 'Proposed'),
        ('approved', 'Approved'),
        ('posted', 'Posted'),
        ], string='Status', default='proposed', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.writeoff') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_posted(self):
        self.write({'state': 'posted'})

