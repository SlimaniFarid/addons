# -*- coding: utf-8 -*-
"""Customer Priority Matrix models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomerClass(models.Model):
    _name = 'sf.customer.class'
    _description = 'Customer Classification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    revenue_class = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ], string='Revenue Class', required=True, default=c)
    strategic_value = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ], string='Strategic Value', default=medium)
    service_level = fields.Selection([
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('standard', 'Standard'),
        ], string='Service Level', default=standard)
    review_date = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('review', 'Under Review'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.class') or 'NEW'
        return super().create(vals_list)

    def action_review(self):
        self.write({'state': 'review'})

