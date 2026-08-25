# -*- coding: utf-8 -*-
"""Sales Coaching Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_coaching_log(models.Model):
    _name = 'sf.sales_coaching_log'
    _description = 'Sales Coaching Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rep_id = fields.Many2one('res.users', string='Sales Rep', required=True)
    coach_id = fields.Many2one('res.users', string='Coach')
    topic = fields.Char(string='Coaching Topic', required=True)
    feedback = fields.Html(string='Feedback')
    next_checkin = fields.Date(string='Next Check-in')
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
                    'sf.sales_coaching_log') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

