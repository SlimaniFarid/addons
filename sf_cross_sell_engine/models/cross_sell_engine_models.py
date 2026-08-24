# -*- coding: utf-8 -*-
"""Cross-Sell Recommendation Engine models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCross_sell_engine(models.Model):
    _name = 'sf.cross_sell_engine'
    _description = 'Cross-Sell Recommendation Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    base_product_id = fields.Many2one('product.product', string='Base Product', required=True)
    recommend_product_id = fields.Many2one('product.product', string='Recommend', required=True)
    affinity_score = fields.Float(string='Affinity Score')
    attach_rate = fields.Float(string='Historical Attach Rate %')
    active = fields.Boolean(string='Active', default=True)
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
                    'sf.cross_sell_engine') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

