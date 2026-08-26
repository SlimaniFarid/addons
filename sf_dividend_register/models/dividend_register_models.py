# -*- coding: utf-8 -*-
"""Dividend Declaration & Payment Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDividend(models.Model):
    _name = 'sf.dividend'
    _description = 'Dividend Declaration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    shareholder_id = fields.Many2one('res.partner', string='Shareholder', required=True)
    declaration_date = fields.Date(string='Declaration Date', default=fields.Date.today)
    per_share_amount = fields.Float(string='Amount per Share')
    shares_held = fields.Float(string='Shares Held')
    gross_amount = fields.Monetary(string='Gross Amount')
    withholding_percent = fields.Float(string='Withholding %')
    payment_date = fields.Date(string='Payment Date')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('declared', 'Declared'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ], string='Status', default='declared', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.dividend') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_paid(self):
        self.write({'state': 'paid'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.dividend'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.dividend'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
