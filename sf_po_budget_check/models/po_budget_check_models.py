# -*- coding: utf-8 -*-
"""PO Budget Check Workflow models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPo_budget_check(models.Model):
    _name = 'sf.po_budget_check'
    _description = 'PO Budget Check Workflow'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    po_id = fields.Many2one('purchase.order', string='Purchase Order', required=True)
    budget_line = fields.Char(string='Budget Line', required=True)
    budget_available = fields.Monetary(string='Budget Available')
    po_amount = fields.Monetary(string='PO Amount')
    over_budget = fields.Boolean(string='Over Budget')
    override_approved = fields.Boolean(string='Override Approved')
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
                    'sf.po_budget_check') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

