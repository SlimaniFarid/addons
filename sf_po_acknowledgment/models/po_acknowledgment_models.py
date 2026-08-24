# -*- coding: utf-8 -*-
"""PO Supplier Acknowledgment models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPo_acknowledgment(models.Model):
    _name = 'sf.po_acknowledgment'
    _description = 'PO Supplier Acknowledgment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    po_id = fields.Many2one('purchase.order', string='Purchase Order', required=True)
    sent_date = fields.Date(string='PO Sent', default=fields.Date.today)
    ack_due_date = fields.Date(string='Acknowledgment Due')
    acknowledged = fields.Boolean(string='Acknowledged')
    chase_count = fields.Integer(string='Chase Count', default=0)
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
                    'sf.po_acknowledgment') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

