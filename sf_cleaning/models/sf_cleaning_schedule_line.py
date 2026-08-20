# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCleaningScheduleLine(models.Model):
    _name = 'sf.cleaning.schedule.line'
    _description = 'Cleaning Schedule Line'
    _order = 'planned_date, id'

    schedule_id = fields.Many2one(
        'sf.cleaning.schedule', string='Schedule', ondelete='cascade',
        required=True, index=True)
    company_id = fields.Many2one(
        'res.company', string='Company', related='schedule_id.company_id',
        store=True, readonly=True)
    task = fields.Char(string='Task')
    planned_date = fields.Date(string='Planned date')
    agent_id = fields.Many2one('res.users', string='Agent')
    start_time = fields.Datetime(string='Start time')
    end_time = fields.Datetime(string='End time')
    executed_date = fields.Date(string='Executed date')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', required=True, tracking=True)
    quality_check_id = fields.Many2one(
        'sf.cleaning.quality_check', string='Quality check',
        ondelete='set null')
    prochaine_date_prevue = fields.Date(
        string='Next planned date', compute='_compute_prochaine_date_prevue',
        store=True)

    @api.depends('planned_date', 'schedule_id.contract_id.line_ids.interval_days',
                 'schedule_id.site_id')
    def _compute_prochaine_date_prevue(self):
        for line in self:
            interval = 7
            if line.schedule_id:
                matching = line.schedule_id.contract_id.line_ids.filtered(
                    lambda l: l.site_id == line.schedule_id.site_id)[:1]
                if matching:
                    interval = matching.interval_days
            line.prochaine_date_prevue = line.planned_date + timedelta(
                days=interval) if line.planned_date else False

    @api.constrains('agent_id', 'planned_date')
    def _check_agent_double_assignment(self):
        for line in self:
            if not line.agent_id or not line.planned_date \
                    or not line.schedule_id.site_id:
                continue
            domain = [
                ('agent_id', '=', line.agent_id.id),
                ('planned_date', '=', line.planned_date),
                ('schedule_id.site_id', '=', line.schedule_id.site_id.id),
                ('id', '!=', line.id),
            ]
            if self.search(domain, limit=1):
                raise UserError(_('An agent cannot be assigned to two '
                                  'interventions on the same site on the '
                                  'same date.'))

    @api.onchange('start_time')
    def _onchange_start_time(self):
        if self.start_time and not self.end_time:
            duration = self.env.company.sf_cleaning_default_duration or 0
            self.end_time = self.start_time + timedelta(hours=duration)

    def action_mark_done(self):
        for line in self:
            if line.state != 'planned':
                raise UserError(_('Only planned interventions can be marked '
                                  'as done.'))
            line.executed_date = fields.Date.context_today(line)
            line.planned_date = line.executed_date
            line.state = 'done'

    def action_cancel_line(self):
        for line in self:
            if line.state != 'planned':
                raise UserError(_('Only planned interventions can be '
                                  'cancelled.'))
        self.state = 'cancelled'