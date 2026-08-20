# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PsaEngagement(models.Model):
    _name = 'sf.psa.engagement'
    _description = 'PSA Engagement'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    partner_id = fields.Many2one('res.partner', string='Client',
                                 required=True)
    project_id = fields.Many2one('project.project', string='Project')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    description = fields.Text(string='Description')
    budget_hours = fields.Float(string='Budget Hours', default=0.0)
    assignment_ids = fields.One2many('sf.psa.assignment', 'engagement_id',
                                     string='Assignments')
    time_entry_ids = fields.One2many('sf.psa.time.entry', 'engagement_id',
                                     string='Time Entries')
    logged_hours = fields.Float(string='Logged Hours', compute='_compute_hours',
                                store=True)
    progress = fields.Float(string='Progress %', compute='_compute_progress',
                            store=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Engagement code must be unique.'),
    ]

    @api.depends('time_entry_ids.hours')
    def _compute_hours(self):
        for eng in self:
            eng.logged_hours = sum(eng.time_entry_ids.mapped('hours'))

    @api.depends('logged_hours', 'budget_hours')
    def _compute_progress(self):
        for eng in self:
            eng.progress = eng.budget_hours and min(
                round((eng.logged_hours / eng.budget_hours) * 100, 1),
                100.0) or 0.0

    def action_start(self):
        for eng in self:
            eng.state = 'active'

    def action_close(self):
        for eng in self:
            eng.state = 'closed'