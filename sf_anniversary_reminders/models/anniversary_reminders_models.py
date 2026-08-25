# -*- coding: utf-8 -*-
"""Anniversary & Birthday Reminders models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAnniversary(models.Model):
    _name = 'sf.anniversary'
    _description = 'Anniversary Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    type = fields.Selection([
        ('anniversary', 'Work Anniversary'),
        ('birthday', 'Birthday'),
        ], string='Type', required=True)
    event_date = fields.Date(string='Event Date (MM-DD)', required=True)
    years = fields.Integer(string='Years')
    celebrated = fields.Boolean(string='Celebrated')
    notes = fields.Char(string='Notes')
    state = fields.Selection([
        ('tracked', 'Tracked'),
        ('celebrated', 'Celebrated'),
        ], string='Status', default='tracked', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.anniversary') or 'NEW'
        return super().create(vals_list)

    def action_celebrated(self):
        self.write({'state': 'celebrated'})

