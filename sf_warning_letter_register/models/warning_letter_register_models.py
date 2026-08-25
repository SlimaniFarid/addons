# -*- coding: utf-8 -*-
"""Employee Warning Letter Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfWarningLetter(models.Model):
    _name = 'sf.warning.letter'
    _description = 'Warning Letter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    severity = fields.Selection([
        ('verbal', 'Verbal'),
        ('written', 'Written'),
        ('final', 'Final Warning'),
        ], string='Severity', required=True, default=written)
    reason = fields.Text(string='Reason', required=True)
    letter_date = fields.Date(string='Letter Date', default=fields.Date.today)
    acknowledged = fields.Boolean(string='Acknowledged by Employee')
    expires_on = fields.Date(string='Active Until')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('acknowledged', 'Acknowledged'),
        ('expired', 'Expired'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.warning.letter') or 'NEW'
        return super().create(vals_list)

    def action_issued(self):
        self.write({'state': 'issued'})

    def action_acknowledged(self):
        self.write({'state': 'acknowledged'})

    def action_expired(self):
        self.write({'state': 'expired'})

