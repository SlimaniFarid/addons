# -*- coding: utf-8 -*-
"""Purchase Order Amendment Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPoAmendment(models.Model):
    _name = 'sf.po.amendment'
    _description = 'PO Amendment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    order_id = fields.Many2one('purchase.order', string='Purchase Order', required=True)
    amendment_type = fields.Selection([
        ('qty', 'Quantity'),
        ('price', 'Price'),
        ('date', 'Date'),
        ('other', 'Other'),
        ], string='Type', required=True)
    before_value = fields.Char(string='Before')
    after_value = fields.Char(string='After')
    reason = fields.Text(string='Reason', required=True)
    approved_by_id = fields.Many2one('res.users', string='Approved By')
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
                    'sf.po.amendment') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

