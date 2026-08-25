# -*- coding: utf-8 -*-
"""Daily Production Meeting Actions models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProductionMeeting(models.Model):
    _name = 'sf.production.meeting'
    _description = 'Production Meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    meeting_date = fields.Date(string='Meeting Date', required=True, default=fields.Date.today)
    chair_id = fields.Many2one('res.users', string='Chair')
    topics = fields.Html(string='Topics Discussed')
    kpi_review = fields.Html(string='KPI Review')
    escalations = fields.Text(string='Escalations')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('held', 'Held'),
        ('actions_tracked', 'Actions Tracked'),
        ('closed', 'Closed'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.production.meeting') or 'NEW'
        return super().create(vals_list)

    def action_held(self):
        self.write({'state': 'held'})

    def action_actions_tracked(self):
        self.write({'state': 'actions_tracked'})

    def action_closed(self):
        self.write({'state': 'closed'})

