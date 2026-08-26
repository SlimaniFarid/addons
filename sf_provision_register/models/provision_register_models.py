# -*- coding: utf-8 -*-
"""Provision Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProvision(models.Model):
    _name = 'sf.provision'
    _description = 'Provision'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    provision_type = fields.Selection([
        ('legal', 'Legal'),
        ('commercial', 'Commercial'),
        ('tax', 'Tax'),
        ('other', 'Other'),
        ], string='Type', required=True)
    period_year = fields.Integer(string='Year')
    amount = fields.Monetary(string='Amount', required=True)
    utilized_amount = fields.Float(string='Utilized')
    reversal_date = fields.Date(string='Reversal Date')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('booked', 'Booked'),
        ('utilized', 'Utilized'),
        ('reversed', 'Reversed'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.provision') or 'NEW'
        return super().create(vals_list)

    def action_booked(self):
        self.write({'state': 'booked'})

    def action_utilized(self):
        self.write({'state': 'utilized'})

    def action_reversed(self):
        self.write({'state': 'reversed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.provision'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.provision'

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
