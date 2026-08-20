# -*- coding: utf-8 -*-
from odoo import fields, models


class VendorContractClause(models.Model):
    _name = 'sf.vendor.contract.clause'
    _description = 'Contract Clause'
    _order = 'contract_id, id'

    contract_id = fields.Many2one('sf.vendor.contract',
                                  string='Contract', required=True,
                                  ondelete='cascade')
    title = fields.Char(string='Title', required=True)
    content = fields.Text(string='Content')
    type = fields.Selection([
        ('pricing', 'Pricing'),
        ('payment', 'Payment'),
        ('penalty', 'Penalty'),
        ('warranty', 'Warranty'),
        ('confidentiality', 'Confidentiality'),
        ('other', 'Other'),
    ], string='Type', default='other')