# -*- coding: utf-8 -*-
"""First-Piece Validation models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFirstPiece(models.Model):
    _name = 'sf.first.piece'
    _description = 'First-Piece Validation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order', required=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center')
    setup_reason = fields.Selection([
        ('new_order', 'New Order'),
        ('tool_change', 'Tool Change'),
        ('material_change', 'Material Change'),
        ('operator_change', 'Operator Change'),
        ], string='Setup Reason', required=True)
    measurements = fields.Html(string='Measurements / Checklist')
    validated = fields.Boolean(string='Production Released')
    inspector_id = fields.Many2one('res.users', string='Inspector')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('pending', 'Pending Validation'),
        ('passed', 'Passed'),
        ('failed', 'Failed - Adjust'),
        ], string='Status', default='pending', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.first.piece') or 'NEW'
        return super().create(vals_list)

    def action_passed(self):
        self.write({'state': 'passed'})

    def action_failed(self):
        self.write({'state': 'failed'})

