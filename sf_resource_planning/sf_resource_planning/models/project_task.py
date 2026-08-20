# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    resource_allocation_ids = fields.One2many(
        'sf.resource.planning.allocation', 'task_id',
        string='Resource Allocations')
    allocated_hours_total = fields.Float(
        string='Allocated Hours', compute='_compute_allocated_hours')

    @api.depends('resource_allocation_ids.hours')
    def _compute_allocated_hours(self):
        for task in self:
            task.allocated_hours_total = sum(
                task.resource_allocation_ids.mapped('hours') or [0.0])