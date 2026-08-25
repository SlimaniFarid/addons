# -*- coding: utf-8 -*-
"""Customer Portal Task Exchange models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPortalTask(models.Model):
    _name = 'sf.portal.task'
    _description = 'Portal Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    title = fields.Char(string='Task Title', required=True)
    requested_from_customer = fields.Text(string='Requested from Customer')
    customer_input = fields.Html(string='Customer Input')
    due_date = fields.Date(string='Due Date')
    validated = fields.Boolean(string='Validated')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('in_progress', 'Customer Working'),
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.portal.task') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_validated(self):
        self.write({'state': 'validated'})

