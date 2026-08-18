# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Resource(models.Model):
    _name = 'sf.resource.planning.resource'
    _description = 'Resource'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    resource_type = fields.Selection([
        ('human', 'Human'),
        ('machine', 'Machine'),
        ('space', 'Space'),
    ], string='Type', default='human', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    user_id = fields.Many2one('res.users', string='User')
    capacity_per_day = fields.Float(
        string='Capacity / Day (h)', default=8.0,
        help="Number of hours available per day for this resource.")
    team_id = fields.Many2one('hr.department', string='Team')
    active = fields.Boolean(string='Active', default=True)
    allocation_ids = fields.One2many(
        'sf.resource.planning.allocation', 'resource_id',
        string='Allocations')
    total_allocated = fields.Float(
        string='Total Allocated (h)', compute='_compute_load')
    utilization = fields.Float(
        string='Utilization (%)', compute='_compute_load')

    @api.depends('allocation_ids.hours', 'capacity_per_day')
    def _compute_load(self):
        for resource in self:
            allocated = sum(resource.allocation_ids.mapped('hours') or [0.0])
            resource.total_allocated = allocated
            if resource.capacity_per_day:
                resource.utilization = round(
                    allocated * 100.0 / resource.capacity_per_day, 1)
            else:
                resource.utilization = 0.0

    def action_open_allocations(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Allocations'),
            'res_model': 'sf.resource.planning.allocation',
            'view_mode': 'tree,form',
            'domain': [('resource_id', '=', self.id)],
        }