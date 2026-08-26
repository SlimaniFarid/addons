# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrecheEnrollment(models.Model):
    _name = 'sf.creche.enrollment'
    _description = 'Creche Enrollment'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Enrollment', required=True, index=True)
    child_id = fields.Many2one('sf.creche.child', string='Child',
                               required=True, ondelete='restrict',
                               index=True)
    room_id = fields.Many2one('sf.creche.room', string='Room',
                              ondelete='restrict')
    enrollment_date = fields.Date(string='Enrollment date',
                                  default=fields.Date.context_today)
    end_date = fields.Date(string='End date')
    monthly_fee = fields.Float(string='Monthly fee')
    hourly_rate = fields.Float(string='Hourly rate')
    schedule = fields.Selection([
        ('full_time', 'Full Time'),
        ('half_day', 'Half Day'),
    ], string='Schedule', default='full_time', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('ended', 'Ended'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.creche.enrollment')
        return super().create(vals)

    def action_activate(self):
        self.ensure_one()
        if not self.user_has_groups('sf_creche.group_sf_creche_manager'):
            raise UserError(_('Only a Creche Manager can activate an '
                              'enrollment.'))
        self.state = 'active'

    def action_end(self):
        self.ensure_one()
        if not self.user_has_groups('sf_creche.group_sf_creche_manager'):
            raise UserError(_('Only a Creche Manager can end an enrollment.'))
        self.state = 'ended'

    def _cron_enrollment_end_reminder(self):
        companies = self.env['res.company'].search([])
        for company in companies:
            ctx_today = fields.Date.context_today(self.with_company(company))
            deadline = ctx_today + timedelta(days=company.sf_creche_alert_days)
            enrollments = self.with_company(company).search([
                ('state', '=', 'active'),
                ('end_date', '!=', False),
                ('end_date', '<=', deadline),
            ])
            for enrollment in enrollments:
                todo = self.env.ref('mail.mail_activity_data_todo')
                existing = enrollment.activity_ids.filtered(
                    lambda a: a.activity_type_id == todo)
                if existing:
                    continue
                enrollment.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Enrollment ending soon: %s')
                    % (enrollment.child_id.name or enrollment.name),
                    user_id=self.env.user.id)
