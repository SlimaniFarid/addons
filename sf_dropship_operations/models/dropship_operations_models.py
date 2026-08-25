# -*- coding: utf-8 -*-
"""Dropshipping Operations Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDropshipOrder(models.Model):
    _name = 'sf.dropship.order'
    _description = 'Dropship Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    vendor_id = fields.Many2one('res.partner', string='Dropship Supplier', required=True)
    product_desc = fields.Char(string='Products')
    supplier_tracking = fields.Char(string='Supplier Tracking')
    notified_date = fields.Date(string='Supplier Notified')
    delivered_date = fields.Date(string='Delivered')
    issues = fields.Text(string='Issues')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('pending', 'Pending Supplier'),
        ('notified', 'Notified'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('issue', 'Issue'),
        ], string='Status', default='pending', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.dropship.order') or 'NEW'
        return super().create(vals_list)

    def action_notified(self):
        self.write({'state': 'notified'})

    def action_shipped(self):
        self.write({'state': 'shipped'})

    def action_delivered(self):
        self.write({'state': 'delivered'})

    def action_issue(self):
        self.write({'state': 'issue'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.dropship.order'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
