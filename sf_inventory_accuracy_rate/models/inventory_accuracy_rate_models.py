# -*- coding: utf-8 -*-
"""Inventory Accuracy KPI models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfInventory_accuracy_rate(models.Model):
    _name = 'sf.inventory_accuracy_rate'
    _description = 'Inventory Accuracy KPI'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    zone = fields.Char(string='Zone', required=True)
    period = fields.Char(string='Period', required=True)
    lines_counted = fields.Integer(string='Lines Counted')
    lines_matched = fields.Integer(string='Lines Matched')
    ira_percent = fields.Float(string='IRA %')
    action_plan = fields.Text(string='Improvement Plan')
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
                    'sf.inventory_accuracy_rate') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

