# -*- coding: utf-8 -*-
"""Mobile Quality Inspection Config models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_inspection_mobile2(models.Model):
    _name = 'sf.quality_inspection_mobile2'
    _description = 'Mobile Quality Inspection Config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    inspection_point = fields.Char(string='Inspection Point', required=True)
    checklist = fields.Html(string='Checklist')
    photo_required = fields.Boolean(string='Photo Required')
    offline_capable = fields.Boolean(string='Offline Capable')
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
                    'sf.quality_inspection_mobile2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

