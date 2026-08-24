# -*- coding: utf-8 -*-
"""Customer Segment Rules Engine models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomerSegment(models.Model):
    _name = 'sf.customer.segment'
    _description = 'Customer Segment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    segment_name = fields.Char(string='Segment', required=True)
    min_revenue = fields.Monetary(string='Min Revenue (12m)')
    max_days_inactive = fields.Integer(string='Max Days Inactive')
    industry = fields.Char(string='Industry Filter')
    member_count = fields.Integer(string='Members')
    last_refresh = fields.Datetime(string='Last Refresh')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('archived', 'Archived'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.segment') or 'NEW'
        return super().create(vals_list)

    def action_archived(self):
        self.write({'state': 'archived'})

