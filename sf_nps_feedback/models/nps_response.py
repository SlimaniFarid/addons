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

    campaign_id = fields.Many2one(required=True, comodel_name='sf.nps.feedback.nps.campaign', ondelete='restrict')
    partner_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    score = fields.Integer(string='Score')
    category = fields.Selection([
        ('promoter', 'Promoter'), ('passive', 'Passive'),
        ('detractor', 'Detractor'),
        ], string='Category', compute='_compute_category', store=True)
    comment = fields.Text(string='Comment')
    response_date = fields.Datetime(string='Response Date', default=fields.Datetime.now)



    @api.depends('score')
    def _compute_category(self):
        for resp in self:
            if resp.score >= 9:
                resp.category = 'promoter'
            elif resp.score >= 7:
                resp.category = 'passive'
            else:
                resp.category = 'detractor'
