# -*- coding: utf-8 -*-
"""Credit Note Reason Analytics models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCreditReason(models.Model):
    _name = 'sf.credit.reason'
    _description = 'Credit Note Reason Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    reason = fields.Selection([
        ('pricing_error', 'Pricing Error'),
        ('quality', 'Quality Issue'),
        ('delivery', 'Delivery Issue'),
        ('commercial', 'Commercial Gesture'),
        ('other', 'Other'),
        ], string='Reason', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    amount = fields.Monetary(string='Credit Amount', required=True)
    root_cause = fields.Text(string='Root Cause')
    corrective_action = fields.Text(string='Corrective Action')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('analyzed', 'Analyzed'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.credit.reason') or 'NEW'
        return super().create(vals_list)

    def action_analyzed(self):
        self.write({'state': 'analyzed'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.credit.reason'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
