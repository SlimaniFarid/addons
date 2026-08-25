# -*- coding: utf-8 -*-
"""Care Workforce Planner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_workforce(models.Model):
    _name = 'sf.customer_care_workforce'
    _description = 'Care Workforce Planner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period = fields.Char(string='Period', required=True)
    forecast_volume = fields.Integer(string='Forecast Volume')
    staff_available = fields.Integer(string='Staff Available')
    staff_needed = fields.Integer(string='Staff Needed')
    skills_gap = fields.Text(string='Skills Gap')
    action = fields.Text(string='Action')
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
                    'sf.customer_care_workforce') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

