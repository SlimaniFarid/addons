# -*- coding: utf-8 -*-
"""Sales Order Freeze Windows models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfOrderFreeze(models.Model):
    _name = 'sf.order.freeze'
    _description = 'Order Freeze Window'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    window_name = fields.Char(string='Window Name', required=True)
    start = fields.Datetime(string='Start', required=True)
    end = fields.Datetime(string='End', required=True)
    scope = fields.Selection([
        ('all', 'All Orders'),
        ('confirmed', 'Confirmed Only'),
        ('invoiced', 'Invoiced Only'),
        ], string='Scope', default=all)
    exception_approvers = fields.Char(string='Exception Approvers')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('ended', 'Ended'),
        ], string='Status', default='scheduled', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.order.freeze') or 'NEW'
        return super().create(vals_list)

    def action_active(self):
        self.write({'state': 'active'})

    def action_ended(self):
        self.write({'state': 'ended'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.order.freeze'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
