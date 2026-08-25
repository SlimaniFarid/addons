# -*- coding: utf-8 -*-
"""Operator Skill Matrix models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfOperatorSkill(models.Model):
    _name = 'sf.operator.skill'
    _description = 'Operator Skill'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Operator', required=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center', required=True)
    skill_name = fields.Char(string='Skill', required=True)
    level = fields.Selection([
        ('1', '1 - Trainee'),
        ('2', '2 - Supervised'),
        ('3', '3 - Autonomous'),
        ('4', '4 - Trainer'),
        ], string='Level', required=True, default=1)
    certified_date = fields.Date(string='Certified')
    expiry_date = fields.Date(string='Expiry')
    training_needed = fields.Boolean(string='Training Needed')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.operator.skill') or 'NEW'
        return super().create(vals_list)

    def action_expired(self):
        self.write({'state': 'expired'})

    def action_revoked(self):
        self.write({'state': 'revoked'})

