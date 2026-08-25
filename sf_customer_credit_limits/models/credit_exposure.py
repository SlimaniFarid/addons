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

    rule_id = fields.Many2one(comodel_name='credit.limit.rule', ondelete='restrict')
    exposure_amount = fields.Monetary(string='Exposure Amount', currency_field='currency_id')
    check_date = fields.Datetime(string='Check Date', default=fields.Datetime.now)
    action_taken = fields.Selection(default='none')

