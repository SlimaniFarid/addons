# -*- coding: utf-8 -*-
"""Fixed Asset Inter-Company Transfer models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFixed_asset_transfer(models.Model):
    _name = 'sf.fixed_asset_transfer'
    _description = 'Fixed Asset Inter-Company Transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    asset_ref = fields.Char(string='Asset Reference', required=True)
    from_company = fields.Char(string='From Entity', required=True)
    to_company = fields.Char(string='To Entity', required=True)
    transfer_value = fields.Monetary(string='Transfer Value')
    transfer_date = fields.Date(string='Transfer Date')
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
                    'sf.fixed_asset_transfer') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

