# -*- coding: utf-8 -*-
"""Supplier Contract Compliance models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfContractCompliance(models.Model):
    _name = 'sf.contract.compliance'
    _description = 'Compliance Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    check_type = fields.Selection([
        ('price', 'Price Compliance'),
        ('sla', 'SLA Adherence'),
        ('quality', 'Quality Terms'),
        ], string='Check', required=True)
    result = fields.Selection([
        ('compliant', 'Compliant'),
        ('deviation', 'Deviation'),
        ('breach', 'Breach'),
        ], string='Result')
    findings = fields.Html(string='Findings')
    corrective = fields.Text(string='Corrective Request')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_review', 'In Review'),
        ('reported', 'Reported'),
        ('closed', 'Closed'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.contract.compliance') or 'NEW'
        return super().create(vals_list)

    def action_in_review(self):
        self.write({'state': 'in_review'})

    def action_reported(self):
        self.write({'state': 'reported'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.contract.compliance'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
