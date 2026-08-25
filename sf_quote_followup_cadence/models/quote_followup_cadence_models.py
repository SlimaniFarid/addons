# -*- coding: utf-8 -*-
"""Quote Follow-up Cadence models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuoteFollowup(models.Model):
    _name = 'sf.quote.followup'
    _description = 'Quote Follow-up'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    order_id = fields.Many2one('sale.order', string='Quotation', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    followup_step = fields.Selection([
        ('d3', 'Day 3'),
        ('d7', 'Day 7'),
        ('d14', 'Day 14'),
        ], string='Step', default=d3)
    due_date = fields.Date(string='Due Date')
    outcome = fields.Text(string='Outcome Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('contacted', 'Contacted'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.quote.followup') or 'NEW'
        return super().create(vals_list)

    def action_contacted(self):
        self.write({'state': 'contacted'})

    def action_won(self):
        self.write({'state': 'won'})

    def action_lost(self):
        self.write({'state': 'lost'})

