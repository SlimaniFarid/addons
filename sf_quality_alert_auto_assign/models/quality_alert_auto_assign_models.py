# -*- coding: utf-8 -*-
"""Quality Alert Auto-Assignment models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_alert_auto_assign(models.Model):
    _name = 'sf.quality_alert_auto_assign'
    _description = 'Quality Alert Auto-Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_category = fields.Char(string='Product Category', required=True)
    defect_type = fields.Char(string='Defect Type')
    assign_team = fields.Char(string='Assign to Team', required=True)
    fallback_user_id = fields.Many2one('res.users', string='Fallback User')
    priority_boost = fields.Boolean(string='Priority Boost')
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
                    'sf.quality_alert_auto_assign') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

