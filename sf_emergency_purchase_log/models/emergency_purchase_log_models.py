# -*- coding: utf-8 -*-
"""Emergency Purchase Workflow models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEmergencyPurchase(models.Model):
    _name = 'sf.emergency.purchase'
    _description = 'Emergency Purchase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    reason = fields.Selection([
        ('breakdown', 'Breakdown'),
        ('stockout', 'Stockout'),
        ('safety', 'Safety'),
        ('other', 'Other'),
        ], string='Emergency Reason', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    retro_po_ref = fields.Char(string='Retro-PO Reference')
    justification = fields.Text(string='Justification', required=True)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('logged', 'Logged'),
        ('approved', 'Approved'),
        ('po_created', 'PO Created'),
        ], string='Status', default='logged', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.emergency.purchase') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_po_created(self):
        self.write({'state': 'po_created'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.emergency.purchase'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
