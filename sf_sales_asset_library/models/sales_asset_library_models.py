# -*- coding: utf-8 -*-
"""Sales Asset Library models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_asset_library(models.Model):
    _name = 'sf.sales_asset_library'
    _description = 'Sales Asset Library'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    asset_title = fields.Char(string='Asset Title', required=True)
    asset_type = fields.Selection([
        ('deck', 'Deck'),
        ('one_pager', 'One-Pager'),
        ('case_study', 'Case Study'),
        ('video', 'Video'),
        ('template', 'Template'),
        ], string='Type', required=True)
    version = fields.Char(string='Version', default=1.0)
    usage_count = fields.Integer(string='Usage Count')
    last_updated = fields.Date(string='Last Updated')
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
                    'sf.sales_asset_library') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

