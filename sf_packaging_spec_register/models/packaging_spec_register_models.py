# -*- coding: utf-8 -*-
"""Packaging Specification Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPackagingSpec(models.Model):
    _name = 'sf.packaging.spec'
    _description = 'Packaging Spec'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    box_type = fields.Char(string='Box Type', required=True)
    units_per_box = fields.Integer(string='Units per Box')
    boxes_per_pallet = fields.Integer(string='Boxes per Pallet')
    label_ref = fields.Char(string='Label Reference')
    revision = fields.Char(string='Spec Revision', default=A)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('obsolete', 'Obsolete'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.packaging.spec') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_obsolete(self):
        self.write({'state': 'obsolete'})

