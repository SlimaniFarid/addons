# -*- coding: utf-8 -*-
"""Change Freeze Calendar models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFreezeWindow(models.Model):
    _name = 'sf.freeze.window'
    _description = 'Freeze Window'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    name = fields.Char(string='Freeze Reason', required=True)
    scope = fields.Selection([
        ('all', 'All Systems'),
        ('production', 'Production Only'),
        ('finance', 'Finance Systems'),
        ], string='Scope', default=all)
    start = fields.Datetime(string='Start', required=True)
    end = fields.Datetime(string='End', required=True)
    exception_process = fields.Text(string='Exception Process')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('ended', 'Ended'),
        ], string='Status', default='scheduled', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.freeze.window') or 'NEW'
        return super().create(vals_list)

    def action_active(self):
        self.write({'state': 'active'})

    def action_ended(self):
        self.write({'state': 'ended'})

