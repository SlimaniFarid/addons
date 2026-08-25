# -*- coding: utf-8 -*-
"""Customer Compliments Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCompliment(models.Model):
    _name = 'sf.compliment'
    _description = 'Customer Compliment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    compliment_date = fields.Date(string='Date', required=True, default=fields.Date.today)
    channel = fields.Selection([
        ('email', 'Email'),
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('survey', 'Survey'),
        ], string='Channel')
    praised_team = fields.Char(string='Team Praised')
    quote = fields.Text(string='Customer Quote', required=True)
    shared_with_team = fields.Boolean(string='Shared with Team')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('received', 'Received'),
        ('shared', 'Shared'),
        ], string='Status', default='received', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.compliment') or 'NEW'
        return super().create(vals_list)

    def action_shared(self):
        self.write({'state': 'shared'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.compliment'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
