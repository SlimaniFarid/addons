# -*- coding: utf-8 -*-
"""Min/Max Parameter Review models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMinmaxReview(models.Model):
    _name = 'sf.minmax.review'
    _description = 'Min/Max Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    current_min = fields.Float(string='Current Min')
    current_max = fields.Float(string='Current Max')
    proposed_min = fields.Float(string='Proposed Min')
    proposed_max = fields.Float(string='Proposed Max')
    evidence = fields.Text(string='Demand Evidence')
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('proposed', 'Proposed'),
        ('approved', 'Approved'),
        ('applied', 'Applied'),
        ('rejected', 'Rejected'),
        ], string='Status', default='proposed', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.minmax.review') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_applied(self):
        self.write({'state': 'applied'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

