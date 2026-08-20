# -*- coding: utf-8 -*-
from odoo import fields, models


class VendorContractVersion(models.Model):
    _name = 'sf.vendor.contract.version'
    _description = 'Contract Version'
    _order = 'contract_id, id'
    _sql_constraints = [
        ('version_unique', 'UNIQUE (contract_id, version)',
         'A version with this number already exists for '
         'this contract.'),
    ]

    contract_id = fields.Many2one('sf.vendor.contract',
                                  string='Contract', required=True,
                                  ondelete='cascade')
    version = fields.Char(string='Version', required=True)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    amount_total = fields.Monetary(string='Total Amount')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self:
                                  self.env.company.currency_id)
    state = fields.Selection([
        ('current', 'Current'),
        ('history', 'History'),
    ], string='Status', default='history')