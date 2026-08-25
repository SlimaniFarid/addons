# -*- coding: utf-8 -*-
"""On-Call Schedule & Escalation models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfOncallSlot(models.Model):
    _name = 'sf.oncall.slot'
    _description = 'On-Call Slot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    member_id = fields.Many2one('res.users', string='On-Call Member', required=True)
    rotation = fields.Char(string='Rotation', required=True)
    start = fields.Datetime(string='Start', required=True)
    end = fields.Datetime(string='End', required=True)
    escalation_level = fields.Integer(string='Escalation Level', default=1)
    override_by_id = fields.Many2one('res.users', string='Overridden By')
    handover_note = fields.Text(string='Handover Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ], string='Status', default='scheduled', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.oncall.slot') or 'NEW'
        return super().create(vals_list)

    def action_active(self):
        self.write({'state': 'active'})

    def action_completed(self):
        self.write({'state': 'completed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.oncall.slot'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
