# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CreditExposure(models.Model):
    _name = 'sf.customer.credit.limits.credit.exposure'
    _description = 'Credit Exposure'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    rule_id = fields.credit.limit.rule(string='Rule Id')
    exposure_amount = fields.Exposure(string='Exposure Amount', currency_field='currency_id')
    check_date = fields.Check(string='Check Date', default=fields.Datetime.now)
    action_taken = fields.none,warned,blocked(string='Action Taken', default='none')

