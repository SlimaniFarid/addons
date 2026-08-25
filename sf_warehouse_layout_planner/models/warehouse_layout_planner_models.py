# -*- coding: utf-8 -*-
"""Warehouse Layout Planner models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfWarehouse_layout_planner(models.Model):
    _name = 'sf.warehouse_layout_planner'
    _description = 'Warehouse Layout Planner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    zone_name = fields.Char(string='Zone', required=True)
    aisle = fields.Char(string='Aisle')
    rack_positions = fields.Integer(string='Rack Positions')
    zone_type = fields.Selection([
        ('picking', 'Picking'),
        ('bulk', 'Bulk Storage'),
        ('staging', 'Staging'),
        ('shipping', 'Shipping'),
        ], string='Type', required=True)
    max_weight_kg = fields.Float(string='Max Weight (kg)')
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
                    'sf.warehouse_layout_planner') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.warehouse_layout_planner'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

