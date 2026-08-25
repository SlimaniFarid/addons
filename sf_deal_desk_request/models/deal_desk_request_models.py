# -*- coding: utf-8 -*-
"""Deal Desk Request models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDeal_desk_request(models.Model):
    _name = 'sf.deal_desk_request'
    _description = 'Deal Desk Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    deal_value = fields.Monetary(string='Deal Value', required=True)
    complexity = fields.Selection([
        ('standard', 'Standard'),
        ('complex', 'Complex'),
        ('strategic', 'Strategic'),
        ], string='Complexity', required=True)
    legal_review = fields.Boolean(string='Legal Review Done')
    finance_review = fields.Boolean(string='Finance Review Done')
    decision = fields.Text(string='Deal Desk Decision')
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
                    'sf.deal_desk_request') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

