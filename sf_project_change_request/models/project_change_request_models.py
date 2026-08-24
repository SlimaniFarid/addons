# -*- coding: utf-8 -*-
"""Project Change Request models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProject_change_request(models.Model):
    _name = 'sf.project_change_request'
    _description = 'Project Change Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    project_name = fields.Char(string='Project', required=True)
    change_description = fields.Text(string='Change Description', required=True)
    cost_impact = fields.Monetary(string='Cost Impact')
    schedule_impact_days = fields.Integer(string='Schedule Impact (days)')
    requested_by_id = fields.Many2one('res.users', string='Requested By')
    approver_id = fields.Many2one('res.users', string='Approver')
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
                    'sf.project_change_request') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

