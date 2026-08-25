# -*- coding: utf-8 -*-
"""Replenishment Review Queue models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfReplenishmentReview(models.Model):
    _name = 'sf.replenishment.review'
    _description = 'Replenishment Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    suggested_qty = fields.Float(string='Suggested Qty')
    adjusted_qty = fields.Float(string='Adjusted Qty')
    demand_note = fields.Text(string='Demand Justification')
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('proposed', 'Proposed'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('rejected', 'Rejected'),
        ], string='Status', default='proposed', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.replenishment.review') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_ordered(self):
        self.write({'state': 'ordered'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.replenishment.review'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
