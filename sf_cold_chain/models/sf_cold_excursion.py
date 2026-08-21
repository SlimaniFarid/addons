# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfColdExcursion(models.Model):
    _name = 'sf.cold.excursion'
    _description = 'Cold Chain Excursion'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.cold.chain.activity.mixin']
    _order = 'started_at asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    trip_id = fields.Many2one('sf.cold.trip', string='Trip', ondelete='cascade')
    site_id = fields.Many2one('sf.cold.site', string='Site', ondelete='cascade')
    started_at = fields.Datetime(string='Started At', required=True)
    ended_at = fields.Datetime(string='Ended At')
    min_temp = fields.Float(string='Min Temp', compute='_compute_details', store=True)
    max_temp = fields.Float(string='Max Temp', compute='_compute_details', store=True)
    duration_minutes = fields.Float(string='Duration (Minutes)',
                                    compute='_compute_details', store=True)
    severity = fields.Selection([
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ], string='Severity', compute='_compute_details', store=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('resolved', 'Resolved'),
    ], string='Status', default='open', copy=False)
    corrective_action = fields.Text(string='Corrective Action')
    resolved_by = fields.Many2one('res.users', string='Resolved By')
    resolved_on = fields.Datetime(string='Resolved On')
    reading_ids = fields.One2many('sf.cold.reading', 'excursion_id',
                                  string='Readings')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.depends('reading_ids.temperature', 'reading_ids.temperature_min',
                 'reading_ids.temperature_max', 'started_at', 'ended_at')
    def _compute_details(self):
        for excursion in self:
            min_temp = 0.0
            max_temp = 0.0
            max_deviation = 0.0
            first = True
            for reading in excursion.reading_ids:
                if not reading.within_range:
                    if first:
                        min_temp = reading.temperature
                        max_temp = reading.temperature
                        first = False
                    else:
                        min_temp = min(min_temp, reading.temperature)
                        max_temp = max(max_temp, reading.temperature)
                    max_deviation = max(max_deviation, reading.deviation)
            excursion.min_temp = min_temp
            excursion.max_temp = max_temp
            # severity: critical if deviation > 20% of range, major if > 10%, minor otherwise
            range_span = 0.0
            if excursion.reading_ids:
                temp_min = excursion.reading_ids[0].temperature_min
                temp_max = excursion.reading_ids[0].temperature_max
                range_span = temp_max - temp_min
            if range_span > 0:
                deviation_pct = (max_deviation / range_span) * 100
                if deviation_pct > 20:
                    excursion.severity = 'critical'
                elif deviation_pct > 10:
                    excursion.severity = 'major'
                else:
                    excursion.severity = 'minor'
            else:
                excursion.severity = 'minor'
            # duration: if ended_at set, use it; else compute ongoing duration to now
            if excursion.ended_at and excursion.started_at:
                duration = excursion.ended_at - excursion.started_at
                excursion.duration_minutes = max(0, duration.total_seconds() / 60)
            elif excursion.started_at:
                duration = fields.Datetime.now() - excursion.started_at
                excursion.duration_minutes = max(0, duration.total_seconds() / 60)
            else:
                excursion.duration_minutes = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.cold.excursion')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_cold_chain.group_sf_cold_chain_manager'):
            raise UserError(_('Only a cold chain manager can resolve excursions.'))

    def action_resolve(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'open':
            raise UserError(_('Only open excursions can be resolved.'))
        end = self.ended_at or (
            max(self.reading_ids.mapped('recorded_at'))
            if self.reading_ids else fields.Datetime.now())
        self.write({
            'state': 'resolved',
            'ended_at': end,
            'resolved_by': self.env.user.id,
            'resolved_on': fields.Datetime.now(),
        })

    def _cron_escalation(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_cold_chain.alert_hours')
        alert_hours = int(param) if param else 24
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            cutoff = fields.Datetime.now() - timedelta(hours=alert_hours)
            excursions = scoped.search([
                ('state', '=', 'open'),
                ('started_at', '<', cutoff),
            ])
            for excursion in excursions:
                excursion._sf_check_todo(
                    todo_type,
                    'Cold excursion %s still open' % excursion.name,
                    'This excursion has been open for more than %s hours.'
                    % alert_hours,
                )