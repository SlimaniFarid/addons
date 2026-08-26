# -*- coding: utf-8 -*-
"""SLA Clock Pause Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSlaPause(models.Model):
    _name = 'sf.sla.pause'
    _description = 'SLA Pause'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    ticket_ref = fields.Char(string='Ticket Reference', required=True)
    pause_reason = fields.Selection([
        ('waiting_customer', 'Waiting for Customer'),
        ('freeze', 'Change Freeze'),
        ('vendor', 'Waiting Vendor'),
        ('other', 'Other'),
        ], string='Reason', required=True)
    paused_at = fields.Datetime(string='Paused At', default=fields.Datetime.now)
    resumed_at = fields.Datetime(string='Resumed At')
    pause_minutes = fields.Float(string='Paused (min)')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('paused', 'Paused'),
        ('resumed', 'Resumed'),
        ], string='Status', default='paused', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.sla.pause') or 'NEW'
        return super().create(vals_list)

    def action_resumed(self):
        self.write({'state': 'resumed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.sla.pause'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
