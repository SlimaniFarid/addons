# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLoanCovenant(models.Model):
    _name = 'sf.loan.covenant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Loan Covenant'
    _order = 'evaluation_date desc, id desc'

    name = fields.Char(string='Number', required=True, index=True)
    covenant_name = fields.Char(string='Name', required=True)
    loan_id = fields.Many2one('sf.loan', string='Loan', required=True,
                              ondelete='cascade', index=True)
    metric = fields.Selection([
        ('debt_ratio', 'Debt Ratio'),
        ('ebitda_cover', 'EBITDA Cover'),
        ('equity', 'Equity'),
        ('other', 'Other'),
    ], string='Metric', default='debt_ratio', required=True)
    formula = fields.Char(string='Formula')
    target_min = fields.Float(string='Target min')
    target_max = fields.Float(string='Target max')
    current_value = fields.Float(string='Current value')
    evaluation_date = fields.Date(string='Evaluation date')
    state = fields.Selection([
        ('active', 'Active'),
        ('breached', 'Breached'),
        ('reviewed', 'Reviewed'),
    ], string='Status', default='active', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='loan_id.company_id', store=True,
                                 readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.loan.covenant')
            vals['name'] = 'COV-%s' % seq
        return super().create(vals)

    def action_check_breach(self):
        self.ensure_one()
        if self.current_value is not False and (
                self.current_value < self.target_min
                or self.current_value > self.target_max):
            self.state = 'breached'
        else:
            self.state = 'active'

    def action_review(self):
        self.ensure_one()
        if self.state != 'breached':
            raise UserError(_('Only breached covenants can be reviewed.'))
        self.state = 'reviewed'