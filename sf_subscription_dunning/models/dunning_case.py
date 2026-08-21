# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DunningCase(models.Model):
    _name = 'sf.subscription.dunning.dunning.case'
    _description = 'Dunning Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    invoice_id = fields.account.move(string='Invoice Id', required=True)
    level_id = fields.dunning.level(string='Level Id')
    attempts = fields.Attempts(string='Attempts', default=0)
    state = fields.open,escalated,resolved(string='State', default='open')

