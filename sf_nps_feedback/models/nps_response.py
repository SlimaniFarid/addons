# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class NpsResponse(models.Model):
    _name = 'sf.nps.feedback.nps.response'
    _description = 'Nps Response'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    campaign_id = fields.nps.campaign(string='Campaign Id', required=True)
    partner_id = fields.res.partner(string='Partner Id')
    score = fields.NPS(string='Score')
    category = fields.promoter,passive,detractor(compute='_compute_category', store=True)
    comment = fields.Comment(string='Comment')
    response_date = fields.Responded(string='Response Date', default=fields.Datetime.now)

