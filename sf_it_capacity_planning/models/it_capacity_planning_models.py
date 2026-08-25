# -*- coding: utf-8 -*-
"""IT Capacity Planning Records models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfItCapacity(models.Model):
    _name = 'sf.it.capacity'
    _description = 'Capacity Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    resource_name = fields.Char(string='Resource', required=True)
    resource_type = fields.Selection([
        ('server', 'Server'),
        ('cloud_vm', 'Cloud VM'),
        ('storage', 'Storage'),
        ('database', 'Database'),
        ], string='Type', required=True)
    cpu_percent = fields.Float(string='CPU % Used')
    ram_percent = fields.Float(string='RAM % Used')
    storage_percent = fields.Float(string='Storage % Used')
    forecast_exhaustion = fields.Date(string='Forecast Exhaustion')
    action_plan = fields.Text(string='Action Plan')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('healthy', 'Healthy'),
        ('watch', 'Watch'),
        ('critical', 'Critical'),
        ], string='Status', default='healthy', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.it.capacity') or 'NEW'
        return super().create(vals_list)

    def action_watch(self):
        self.write({'state': 'watch'})

    def action_critical(self):
        self.write({'state': 'critical'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.it.capacity'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
