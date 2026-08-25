# -*- coding: utf-8 -*-
"""Quality Hold & Quarantine Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQualityHold(models.Model):
    _name = 'sf.quality.hold'
    _description = 'Quality Hold'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Lot')
    quantity = fields.Float(string='Quantity on Hold')
    hold_reason = fields.Selection([
        ('customer_claim', 'Customer Claim'),
        ('internal_finding', 'Internal Finding'),
        ('supplier_issue', 'Supplier Issue'),
        ], string='Reason', required=True)
    investigation_ref = fields.Char(string='Investigation Ref')
    release_decision = fields.Text(string='Release / Scrap Decision')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('held', 'Held'),
        ('investigating', 'Investigating'),
        ('released', 'Released'),
        ('scrapped', 'Scrapped'),
        ], string='Status', default='held', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.quality.hold') or 'NEW'
        return super().create(vals_list)

    def action_investigating(self):
        self.write({'state': 'investigating'})

    def action_released(self):
        self.write({'state': 'released'})

    def action_scrapped(self):
        self.write({'state': 'scrapped'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.quality.hold'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
