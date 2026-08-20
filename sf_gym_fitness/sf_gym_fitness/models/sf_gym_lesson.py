# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfGymLesson(models.Model):
    _name = 'sf.gym.lesson'
    _description = 'Gym Lesson'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    plan_ids = fields.Many2many(
        'sf.gym.plan', string='Plans')
    capacity = fields.Integer(string='Capacity', default=10)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.gym.lesson')
        return super().create(vals)
