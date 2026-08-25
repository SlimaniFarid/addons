# -*- coding: utf-8 -*-
"""Customer Pricing Request Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPricingRequest(models.Model):
    _name = 'sf.pricing.request'
    _description = 'Pricing Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    requested_qty = fields.Float(string='Requested Qty')
    quoted_price = fields.Float(string='Quoted Price')
    target_price = fields.Float(string='Customer Target Price')
    response_hours = fields.Float(string='Response Time (h)')
    outcome = fields.Selection([
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ], string='Outcome', default=pending)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('received', 'Received'),
        ('quoted', 'Quoted'),
        ('decided', 'Decided'),
        ], string='Status', default='received', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.pricing.request') or 'NEW'
        return super().create(vals_list)

    def action_quoted(self):
        self.write({'state': 'quoted'})

    def action_decided(self):
        self.write({'state': 'decided'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.pricing.request'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
