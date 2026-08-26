# -*- coding: utf-8 -*-
"""Cross-Dock Operations Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCrossdock(models.Model):
    _name = 'sf.crossdock'
    _description = 'Cross-Dock Operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    inbound_ref = fields.Char(string='Inbound Ref', required=True)
    outbound_ref = fields.Char(string='Outbound Ref')
    arrival_at = fields.Datetime(string='Arrival', default=fields.Datetime.now)
    departure_at = fields.Datetime(string='Departure')
    dwell_hours = fields.Float(string='Dwell (h)')
    priority = fields.Selection([
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ], string='Priority', default=normal)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('arrived', 'Arrived'),
        ('staged', 'Staged'),
        ('departed', 'Departed'),
        ], string='Status', default='arrived', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.crossdock') or 'NEW'
        return super().create(vals_list)

    def action_staged(self):
        self.write({'state': 'staged'})

    def action_departed(self):
        self.write({'state': 'departed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.crossdock'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.crossdock'

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
