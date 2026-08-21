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

    invoice_id = fields.Many2one(required=True, comodel_name='account.move', ondelete='restrict')
    level_id = fields.Many2one(comodel_name='dunning.level', ondelete='restrict')
    attempts = fields.Integer(string='Attempts', default=0)
    state = fields.Selection(default='open')

