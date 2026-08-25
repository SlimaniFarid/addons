# -*- coding: utf-8 -*-
"""Customer Care Touch Program models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCareTouch(models.Model):
    _name = 'sf.care.touch'
    _description = 'Care Touch Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    cadence_days = fields.Integer(string='Cadence (days)', default=90)
    last_touch = fields.Date(string='Last Touch')
    next_touch = fields.Date(string='Next Touch')
    touch_type = fields.Selection([
        ('call', 'Call'),
        ('visit', 'Visit'),
        ('meal', 'Business Meal'),
        ('survey', 'Survey'),
        ], string='Touch Type', default=call)
    satisfaction = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ], string='Satisfaction')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('skipped', 'Skipped'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.care.touch') or 'NEW'
        return super().create(vals_list)

    def action_done(self):
        self.write({'state': 'done'})

    def action_skipped(self):
        self.write({'state': 'skipped'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.care.touch'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

