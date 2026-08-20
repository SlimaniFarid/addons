# -*- coding: utf-8 -*-
from odoo import fields, models, _


class ConsolidationLine(models.Model):
    _name = 'sf.consolidation.line'
    _description = 'Consolidation Line'
    _order = 'account_id, company_id'

    period_id = fields.Many2one('sf.consolidation.period', string='Period',
                                required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True)
    account_id = fields.Many2one('account.account', string='Account',
                                 required=True)
    amount = fields.Float(string='Amount', required=True, default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id',
                                  readonly=True)