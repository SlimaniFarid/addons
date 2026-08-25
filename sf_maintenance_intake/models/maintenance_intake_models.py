# -*- coding: utf-8 -*-
"""Maintenance Request Intake models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMaintenanceIntake(models.Model):
    _name = 'sf.maintenance.intake'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    description = fields.Text(string='Issue Description', required=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
        ], string='Priority', required=True, default=normal)
    requested_by_id = fields.Many2one('res.users', string='Requested By')
    assigned_team = fields.Char(string='Assigned Team')
    resolution_note = fields.Text(string='Resolution')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('submitted', 'Submitted'),
        ('triaged', 'Triaged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ], string='Status', default='submitted', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.maintenance.intake') or 'NEW'
        return super().create(vals_list)

    def action_triaged(self):
        self.write({'state': 'triaged'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_resolved(self):
        self.write({'state': 'resolved'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.maintenance.intake'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
