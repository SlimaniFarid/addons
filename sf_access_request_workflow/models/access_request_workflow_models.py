# -*- coding: utf-8 -*-
"""Access Request Workflow models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAccess_request_workflow(models.Model):
    _name = 'sf.access_request_workflow'
    _description = 'Access Request Workflow'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    requester_id = fields.Many2one('res.users', string='Requester', required=True)
    system_name = fields.Char(string='System', required=True)
    access_level = fields.Selection([
        ('read', 'Read Only'),
        ('write', 'Read/Write'),
        ('admin', 'Admin'),
        ], string='Level', required=True)
    justification = fields.Text(string='Justification', required=True)
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
                    'sf.access_request_workflow') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

