# -*- coding: utf-8 -*-
"""Disciplinary Action Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDisciplinary_action(models.Model):
    _name = 'sf.disciplinary_action'
    _description = 'Disciplinary Action Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    action_type = fields.Selection([
        ('verbal', 'Verbal'),
        ('written', 'Written'),
        ('suspension', 'Suspension'),
        ('termination', 'Termination'),
        ], string='Type', required=True)
    action_date = fields.Date(string='Date', default=fields.Date.today)
    description = fields.Text(string='Description', required=True)
    expiry_date = fields.Date(string='Expires On')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.disciplinary_action') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

