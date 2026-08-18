# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PsaAssignment(models.Model):
    _name = 'sf.psa.assignment'
    _description = 'PSA Assignment'
    _rec_name = 'resource_id'

    engagement_id = fields.Many2one('sf.psa.engagement', string='Engagement',
                                    required=True, ondelete='cascade')
    resource_id = fields.Many2one('sf.psa.resource', string='Resource',
                                  required=True)
    role = fields.Char(string='Role')
    allocated_hours = fields.Float(string='Allocated Hours', default=0.0)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    time_entry_ids = fields.One2many('sf.psa.time.entry', 'assignment_id',
                                     string='Time Entries')
    logged_hours = fields.Float(string='Logged Hours', compute='_compute_hours',
                                store=True)
    utilization = fields.Float(string='Utilization %',
                               compute='_compute_utilization', store=True)

    @api.depends('time_entry_ids.hours')
    def _compute_hours(self):
        for assign in self:
            assign.logged_hours = sum(assign.time_entry_ids.mapped('hours'))

    @api.depends('logged_hours', 'allocated_hours')
    def _compute_utilization(self):
        for assign in self:
            assign.utilization = assign.allocated_hours and min(
                round((assign.logged_hours / assign.allocated_hours) * 100,
                      1), 100.0) or 0.0