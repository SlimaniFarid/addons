# -*- coding: utf-8 -*-
"""Stock Adjustment Approval models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAdjustmentRequest(models.Model):
    _name = 'sf.adjustment.request'
    _description = 'Adjustment Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Qty Adjusted')
    value = fields.Monetary(string='Value Impact')
    reason_code = fields.Selection([
        ('count', 'Cycle Count'),
        ('damage', 'Damage'),
        ('theft', 'Theft/Suspected'),
        ('process', 'Process Error'),
        ('other', 'Other'),
        ], string='Reason', required=True)
    requested_by_id = fields.Many2one('res.users', string='Requested By')
    approver_id = fields.Many2one('res.users', string='Approver')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.adjustment.request') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

