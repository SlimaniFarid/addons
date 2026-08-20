# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResourceAllocation(models.Model):
    _name = 'sf.resource.planning.allocation'
    _description = 'Resource Allocation'
    _order = 'date_start'

    resource_id = fields.Many2one(
        'sf.resource.planning.resource', string='Resource', required=True,
        ondelete='cascade')
    task_id = fields.Many2one('project.task', string='Task')
    project_id = fields.Many2one(
        'project.project', string='Project', related='task_id.project_id',
        store=True)
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date')
    hours = fields.Float(string='Hours', required=True, default=8.0)
    note = fields.Text(string='Note')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)

    @api.constrains('hours')
    def _check_hours(self):
        for alloc in self:
            if alloc.hours <= 0:
                raise models.ValidationError(
                    _('Allocation hours must be positive.'))

    @api.onchange('task_id')
    def _onchange_task(self):
        if self.task_id:
            self.date_start = self.task_id.date_deadline or self.date_start