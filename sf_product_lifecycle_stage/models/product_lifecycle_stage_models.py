# -*- coding: utf-8 -*-
"""Product Lifecycle Stage Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduct_lifecycle_stage(models.Model):
    _name = 'sf.product_lifecycle_stage'
    _description = 'Product Lifecycle Stage Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    stage = fields.Selection([
        ('introduction', 'Introduction'),
        ('growth', 'Growth'),
        ('maturity', 'Maturity'),
        ('decline', 'Decline'),
        ('end_of_life', 'End of Life'),
        ], string='Stage', required=True)
    strategy = fields.Text(string='Stage Strategy')
    review_date = fields.Date(string='Next Review')
    owner_id = fields.Many2one('res.users', string='Product Manager')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.product_lifecycle_stage') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

