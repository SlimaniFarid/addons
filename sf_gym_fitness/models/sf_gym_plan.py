# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfGymPlan(models.Model):
    _name = 'sf.gym.plan'
    _description = 'Gym Plan'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    code = fields.Char(string='Code', tracking=True)
    price_monthly = fields.Float(
        string='Monthly price', required=True, tracking=True)
    duration_months = fields.Integer(
        string='Duration (months)', required=True, tracking=True)
    lesson_ids = fields.Many2many(
        'sf.gym.lesson', string='Lessons')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not self.env.user.has_group(
                'sf_gym_fitness.group_sf_gym_manager'):
            raise UserError(_('Only a gym manager can create plans.'))
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.gym.plan')
        return super().create(vals)

    def write(self, vals):
        if not self.env.user.has_group(
                'sf_gym_fitness.group_sf_gym_manager'):
            raise UserError(_('Only a gym manager can modify plans.'))
        return super().write(vals)
