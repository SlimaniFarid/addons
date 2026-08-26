# -*- coding: utf-8 -*-
"""Financial Covenant Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCovenant(models.Model):
    _name = 'sf.covenant'
    _description = 'Covenant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    lender = fields.Char(string='Lender', required=True)
    covenant_type = fields.Selection([
        ('debt_ebitda', 'Debt / EBITDA'),
        ('interest_cover', 'Interest Coverage'),
        ('current_ratio', 'Current Ratio'),
        ('other', 'Other'),
        ], string='Type', required=True)
    threshold = fields.Float(string='Threshold')
    actual_value = fields.Float(string='Actual')
    test_date = fields.Date(string='Test Date')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('compliant', 'Compliant'),
        ('breached', 'Breached'),
        ('waived', 'Waived'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.covenant') or 'NEW'
        return super().create(vals_list)

    def action_compliant(self):
        self.write({'state': 'compliant'})

    def action_breached(self):
        self.write({'state': 'breached'})

    def action_waived(self):
        self.write({'state': 'waived'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.covenant'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.covenant'

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
