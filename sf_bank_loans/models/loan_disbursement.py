# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfLoanDisbursement(models.Model):
    _name = 'sf.loan.disbursement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Loan Disbursement'
    _order = 'date desc, id desc'

    name = fields.Char(string='Number', required=True, index=True)
    loan_id = fields.Many2one('sf.loan', string='Loan', required=True,
                              ondelete='cascade', index=True)
    amount = fields.Float(string='Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.today,
                       required=True)
    reference = fields.Char(string='Reference')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='loan_id.company_id', store=True,
                                 readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.loan.disbursement')
            vals['name'] = 'DIS-%s' % seq
        rec = super().create(vals)
        rec.loan_id.action_disburse()
        return rec