# -*- coding: utf-8 -*-
"""Committee Decision Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCommitteeDecision(models.Model):
    _name = 'sf.committee.decision'
    _description = 'Committee Decision'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    committee = fields.Char(string='Committee', required=True)
    meeting_date = fields.Date(string='Meeting Date', required=True)
    topic = fields.Char(string='Topic', required=True)
    context = fields.Html(string='Context & Options')
    decision = fields.Text(string='Decision', required=True)
    followup_actions = fields.Text(string='Follow-up Actions')
    chair_id = fields.Many2one('res.users', string='Chair')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('executed', 'Executed'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.committee.decision') or 'NEW'
        return super().create(vals_list)

    def action_confirmed(self):
        self.write({'state': 'confirmed'})

    def action_executed(self):
        self.write({'state': 'executed'})

