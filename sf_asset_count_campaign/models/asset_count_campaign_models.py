# -*- coding: utf-8 -*-
"""Fixed Asset Physical Count models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAssetCount(models.Model):
    _name = 'sf.asset.count'
    _description = 'Asset Count Campaign'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    location = fields.Char(string='Location / Site', required=True)
    count_date = fields.Date(string='Count Date', default=fields.Date.today)
    assets_expected = fields.Integer(string='Assets in Ledger')
    assets_found = fields.Integer(string='Assets Found')
    missing_count = fields.Integer(string='Missing')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('counting', 'Counting'),
        ('reconciled', 'Reconciled'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.asset.count') or 'NEW'
        return super().create(vals_list)

    def action_counting(self):
        self.write({'state': 'counting'})

    def action_reconciled(self):
        self.write({'state': 'reconciled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.asset.count'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.asset.count'

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
