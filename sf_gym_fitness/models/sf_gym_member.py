# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfGymMember(models.Model):
    _name = 'sf.gym.member'
    _description = 'Gym Member'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='set null', index=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    birth_date = fields.Date(string='Birth date')
    photo = fields.Binary(string='Photo')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.gym.member')
        return super().create(vals)
