# -*- coding: utf-8 -*-
"""FX Revaluation Scheduler models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFxReval(models.Model):
    _name = 'sf.fx.reval'
    _description = 'FX Revaluation Run'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period_month = fields.Date(string='Period', default=fields.Date.today)
    total_gain = fields.Float(string='Total Unrealized Gain')
    total_loss = fields.Float(string='Total Unrealized Loss')
    item_count = fields.Integer(string='Open FX Items')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Computed'),
        ('posted', 'Posted'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.fx.reval') or 'NEW'
        return super().create(vals_list)

    def action_computed(self):
        self.write({'state': 'computed'})

    def action_posted(self):
        self.write({'state': 'posted'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.fx.reval'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
