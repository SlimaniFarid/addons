# -*- coding: utf-8 -*-
"""BOM Change Requests models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBomChange(models.Model):
    _name = 'sf.bom.change'
    _description = 'BOM Change Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    bom_id = fields.Many2one('mrp.bom', string='BoM', required=True)
    change_description = fields.Text(string='Change Description', required=True)
    cost_impact = fields.Monetary(string='Cost Impact / Unit')
    effectivity_date = fields.Date(string='Effectivity Date')
    approver_id = fields.Many2one('res.users', string='Approved By')
    reason = fields.Selection([
        ('cost', 'Cost Reduction'),
        ('quality', 'Quality'),
        ('supply', 'Supply Issue'),
        ('other', 'Other'),
        ], string='Reason')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Review'),
        ('approved', 'Approved'),
        ('implemented', 'Implemented'),
        ('rejected', 'Rejected'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.bom.change') or 'NEW'
        return super().create(vals_list)

    def action_review(self):
        self.write({'state': 'review'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_implemented(self):
        self.write({'state': 'implemented'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

