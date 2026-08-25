# -*- coding: utf-8 -*-
"""Decision Log with Context models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDecision(models.Model):
    _name = 'sf.decision'
    _description = 'Decision Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Decision Title', required=True)
    date = fields.Date(string='Decision Date', required=True, default=fields.Date.today)
    context = fields.Html(string='Context & Options')
    rationale = fields.Text(string='Rationale')
    decision_maker_id = fields.Many2one('res.users', string='Decision Maker')
    review_date = fields.Date(string='Review If Still Valid')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('recorded', 'Recorded'),
        ('superseded', 'Superseded'),
        ], string='Status', default='recorded', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.decision') or 'NEW'
        return super().create(vals_list)

    def action_superseded(self):
        self.write({'state': 'superseded'})

