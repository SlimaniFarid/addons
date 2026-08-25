# -*- coding: utf-8 -*-
"""Employee Asset Return Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfAssetReturn(models.Model):
    _name = 'sf.asset.return'
    _description = 'Asset Return'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    asset_type = fields.Selection([
        ('laptop', 'Laptop'),
        ('phone', 'Phone'),
        ('badge', 'Badge'),
        ('car', 'Vehicle'),
        ('other', 'Other'),
        ], string='Asset', required=True)
    return_due = fields.Date(string='Return Due', required=True)
    returned_date = fields.Date(string='Returned')
    condition = fields.Selection([
        ('good', 'Good'),
        ('damaged', 'Damaged'),
        ('missing', 'Missing'),
        ], string='Condition')
    deposit_released = fields.Boolean(string='Deposit Released')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('pending', 'Pending Return'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ], string='Status', default='pending', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.asset.return') or 'NEW'
        return super().create(vals_list)

    def action_returned(self):
        self.write({'state': 'returned'})

    def action_overdue(self):
        self.write({'state': 'overdue'})

