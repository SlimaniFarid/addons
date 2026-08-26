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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.resource.planning.resource'

    def action_refresh_business(self):
        """Pull employee tenure and status."""
        for rec in self:
            emp = getattr(rec, 'employee_id', False)
            if not emp:
                continue
            hire = emp.first_contract_date or False
            years = ''
            if hire:
                delta = (fields.Date.context_today(rec) - hire).days
                years = ', tenure {:.1f}y'.format(delta / 365.25)
            rec.message_post(body=_('{name} ({dept}){tenure}, '
                                    'active={act}.').format(
                name=emp.name,
                dept=emp.department_id.name or '-',
                tenure=years,
                act=emp.active))
        return True
