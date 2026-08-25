# -*- coding: utf-8 -*-
"""Procurement Savings Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProcurement_savings_tracker(models.Model):
    _name = 'sf.procurement_savings_tracker'
    _description = 'Procurement Savings Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    initiative = fields.Char(string='Initiative', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    savings_type = fields.Selection([
        ('price', 'Price Reduction'),
        ('consolidation', 'Volume Consolidation'),
        ('process', 'Process Improvement'),
        ('substitution', 'Product Substitution'),
        ], string='Type', required=True)
    annual_savings = fields.Monetary(string='Annual Savings', required=True)
    implemented_date = fields.Date(string='Implemented')
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
                    'sf.procurement_savings_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.procurement_savings_tracker'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

