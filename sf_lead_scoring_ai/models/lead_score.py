# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LeadScore(models.Model):
    _name = 'sf.lead.scoring.ai.lead.score'
    _description = 'Lead Score'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    lead_id = fields.crm.lead(string='Lead Id', required=True)
    total_score = fields.Total(string='Total Score')
    grade = fields.A,B,C,D(string='Grade', default='D')
    scored_date = fields.Scored(string='Scored Date', default=fields.Datetime.now)

