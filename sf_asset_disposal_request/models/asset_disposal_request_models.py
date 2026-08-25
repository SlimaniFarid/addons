# -*- coding: utf-8 -*-
"""Asset Disposal Request models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAsset_disposal_request(models.Model):
    _name = 'sf.asset_disposal_request'
    _description = 'Asset Disposal Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    asset_ref = fields.Char(string='Asset Reference', required=True)
    disposal_reason = fields.Selection([
        ('obsolete', 'Obsolete'),
        ('damaged', 'Damaged'),
        ('sold', 'Sold'),
        ('donated', 'Donated'),
        ], string='Reason', required=True)
    book_value = fields.Monetary(string='Book Value')
    disposal_value = fields.Monetary(string='Disposal Value')
    approved_by_id = fields.Many2one('res.users', string='Approved By')
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
                    'sf.asset_disposal_request') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

