# -*- coding: utf-8 -*-
"""Meeting Minutes & Action Items models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMeetingMinutes(models.Model):
    _name = 'sf.meeting.minutes'
    _description = 'Meeting Minutes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Meeting', required=True)
    meeting_date = fields.Date(string='Date', required=True, default=fields.Date.today)
    chair_id = fields.Many2one('res.users', string='Chair')
    attendees = fields.Text(string='Attendees')
    decisions = fields.Html(string='Decisions')
    action_items = fields.Html(string='Action Items')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('distributed', 'Distributed'),
        ('actions_done', 'Actions Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.meeting.minutes') or 'NEW'
        return super().create(vals_list)

    def action_distributed(self):
        self.write({'state': 'distributed'})

    def action_actions_done(self):
        self.write({'state': 'actions_done'})

