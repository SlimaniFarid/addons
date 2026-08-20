# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLoanRepayment(models.Model):
    _name = 'sf.loan.repayment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Loan Early Repayment'
    _order = 'date desc, id desc'

    name = fields.Char(string='Number', required=True, index=True)
    loan_id = fields.Many2one('sf.loan', string='Loan', required=True,
                              ondelete='cascade', index=True)
    amount = fields.Float(string='Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.today,
                       required=True)
    reason = fields.Char(string='Reason')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='loan_id.company_id', store=True,
                                 readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.loan.repayment')
            vals['name'] = 'REP-%s' % seq
        return super().create(vals)

    def action_confirm(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_bank_loans.group_loan_manager'):
            raise UserError(_('Only loan managers can validate early '
                              'repayments.'))
        self.state = 'done'
        self.loan_id._apply_early_repayment(self.amount)