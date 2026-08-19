# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfLoanBank(models.Model):
    _name = 'sf.loan.bank'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Loan Bank'
    _order = 'name'

    name = fields.Char(string='Number', required=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Bank',
                                 ondelete='restrict')
    contact = fields.Char(string='Contact')
    phone = fields.Char(string='Phone')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         'This bank number already exists.'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.loan.bank')
            vals['name'] = 'BNK-%s' % seq
        return super().create(vals)