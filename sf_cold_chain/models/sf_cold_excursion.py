# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfColdExcursion(models.Model):
    _name = 'sf.cold.excursion'
    _description = 'Cold Chain Excursion'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.cold.chain.activity.mixin']
    _order = 'start_datetime asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    trip_id = fields.Many2one('sf.cold.trip', string='Trip', ondelete='cascade')
    site_id = fields.Many2one('sf.cold.site', string='Site', ondelete='cascade')
    start_datetime = fields.Datetime(string='Start', required=True)
    end_datetime = fields.Datetime(string='End')
    duration_minutes = fields.Integer(string='Duration (Minutes)',
                                      compute='_compute_details', store=True)
    max_deviation = fields.Float(string='Max Deviation',
                                 compute='_compute_details', store=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Severity', compute='_compute_details', store=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('resolved', 'Resolved'),
    ], string='Status', default='open', copy=False)
    resolved_by = fields.Many2one('res.users', string='Resolved By')
    resolved_datetime = fields.Datetime(string='Resolved On')
    resolution_note = fields.Text(string='Resolution Note')
    reading_ids = fields.One2many('sf.cold.reading', 'excursion_id',
                                  string='Readings')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.depends('reading_ids.temperature', 'reading_ids.temperature_min',
                 'reading_ids.temperature_max', 'start_datetime', 'end_datetime')
    def _compute_details(self):
        for excursion in self:
            deviation = 0.0
            for reading in excursion.reading_ids:
                if not reading.within_range:
                    deviation = max(deviation, reading.deviation)
            excursion.max_deviation = deviation
            if deviation >= 5.0:
                excursion.severity = 'high'
            elif deviation >= 2.0:
                excursion.severity = 'medium'
            else:
                excursion.severity = 'low'
            if excursion.end_datetime and excursion.start_datetime:
                duration = excursion.end_datetime - excursion.start_datetime
                excursion.duration_minutes = int(max(0, duration.total_seconds() // 60))
            else:
                excursion.duration_minutes = 0

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
        end = self.end_datetime or (
            max(self.reading_ids.mapped('reading_datetime'))
            if self.reading_ids else fields.Datetime.now())
        self.write({
            'state': 'resolved',
            'end_datetime': end,
            'resolved_by': self.env.user.id,
            'resolved_datetime': fields.Datetime.now(),
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
                ('start_datetime', '<', cutoff),
            ])
            for excursion in excursions:
                excursion._sf_check_todo(
                    todo_type,
                    'Cold excursion %s still open' % excursion.name,
                    'This excursion has been open for more than %s hours.'
                    % alert_hours,
                )