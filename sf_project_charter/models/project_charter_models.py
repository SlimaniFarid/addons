# -*- coding: utf-8 -*-
"""Project Charter Manager models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProject_charter(models.Model):
    _name = 'sf.project_charter'
    _description = 'Project Charter Manager'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    project_name = fields.Char(string='Project Name', required=True)
    objectives = fields.Html(string='Objectives')
    scope = fields.Html(string='Scope')
    budget = fields.Monetary(string='Budget')
    sponsor_id = fields.Many2one('res.users', string='Sponsor')
    start_date = fields.Date(string='Start')
    end_date = fields.Date(string='End')
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
                    'sf.project_charter') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

