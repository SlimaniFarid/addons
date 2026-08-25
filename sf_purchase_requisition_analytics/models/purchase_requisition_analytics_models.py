# -*- coding: utf-8 -*-
"""Requisition Analytics models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPurchase_requisition_analytics(models.Model):
    _name = 'sf.purchase_requisition_analytics'
    _description = 'Requisition Analytics'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period = fields.Char(string='Period', required=True)
    total_requisitions = fields.Integer(string='Total Requisitions')
    approved_count = fields.Integer(string='Approved')
    rejected_count = fields.Integer(string='Rejected')
    avg_approval_days = fields.Float(string='Avg Approval (days)')
    top_requester = fields.Char(string='Top Requester')
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
                    'sf.purchase_requisition_analytics') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

