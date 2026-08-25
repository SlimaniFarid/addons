# -*- coding: utf-8 -*-
"""Production Order Sequencing models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_order_sequencing(models.Model):
    _name = 'sf.production_order_sequencing'
    _description = 'Production Order Sequencing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order', required=True)
    sequence_no = fields.Integer(string='Sequence', required=True)
    priority_score = fields.Float(string='Priority Score')
    changeover_minutes = fields.Float(string='Changeover (min)')
    due_date = fields.Date(string='Due Date')
    optimization_note = fields.Text(string='Optimization Notes')
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
                    'sf.production_order_sequencing') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

