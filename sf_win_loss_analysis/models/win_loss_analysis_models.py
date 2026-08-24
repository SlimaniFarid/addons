# -*- coding: utf-8 -*-
"""Win / Loss Analysis Library models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfWinLoss(models.Model):
    _name = 'sf.win.loss'
    _description = 'Win / Loss Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    outcome = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ], string='Outcome', required=True)
    primary_reason = fields.Selection([
        ('price', 'Price'),
        ('quality', 'Quality'),
        ('delay', 'Lead Time'),
        ('relationship', 'Relationship'),
        ('other', 'Other'),
        ], string='Primary Reason')
    competitor = fields.Char(string='Competitor')
    price_gap_percent = fields.Float(string='Price Gap %')
    lessons = fields.Html(string='Lessons Learned')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('analyzed', 'Analyzed'),
        ('shared', 'Shared'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.win.loss') or 'NEW'
        return super().create(vals_list)

    def action_analyzed(self):
        self.write({'state': 'analyzed'})

    def action_shared(self):
        self.write({'state': 'shared'})

