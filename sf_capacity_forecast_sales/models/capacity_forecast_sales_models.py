# -*- coding: utf-8 -*-
"""Sales Capacity Forecast models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSalesCapacity(models.Model):
    _name = 'sf.sales.capacity'
    _description = 'Sales Capacity Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period_month = fields.Date(string='Period', required=True)
    team_lead_id = fields.Many2one('res.users', string='Team Lead')
    active_reps = fields.Integer(string='Active Reps')
    working_days = fields.Integer(string='Working Days')
    meetings_target = fields.Integer(string='Meetings Target')
    pipeline_target = fields.Monetary(string='Pipeline Target')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('locked', 'Locked'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.sales.capacity') or 'NEW'
        return super().create(vals_list)

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

    def action_locked(self):
        self.write({'state': 'locked'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.sales.capacity'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
