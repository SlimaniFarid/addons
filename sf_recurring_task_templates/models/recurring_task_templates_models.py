# -*- coding: utf-8 -*-
"""Recurring Task Templates models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRecurringTask(models.Model):
    _name = 'sf.recurring.task'
    _description = 'Recurring Task Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Task Title', required=True)
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ], string='Frequency', required=True, default=weekly)
    owner_id = fields.Many2one('res.users', string='Owner')
    instructions = fields.Html(string='Instructions')
    last_done = fields.Date(string='Last Done')
    next_due = fields.Date(string='Next Due')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('retired', 'Retired'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.recurring.task') or 'NEW'
        return super().create(vals_list)

    def action_paused(self):
        self.write({'state': 'paused'})

    def action_retired(self):
        self.write({'state': 'retired'})

