# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfGymSession(models.Model):
    _name = 'sf.gym.session'
    _description = 'Gym Session'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    lesson_id = fields.Many2one(
        'sf.gym.lesson', string='Lesson', ondelete='restrict',
        index=True, tracking=True, required=True)
    coach_id = fields.Many2one(
        'res.users', string='Coach', ondelete='set null',
        index=True, tracking=True)
    date = fields.Date(
        string='Date', default=fields.Date.context_today,
        required=True, tracking=True)
    start_time = fields.Float(string='Start time')
    capacity = fields.Integer(
        string='Capacity', compute='_compute_capacity')
    attendance_ids = fields.One2many(
        'sf.gym.attendance', 'session_id', string='Attendances')
    attendance_count = fields.Integer(
        string='Attendances', compute='_compute_attendance_count',
        store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('lesson_id.capacity')
    def _compute_capacity(self):
        for session in self:
            session.capacity = session.lesson_id.capacity

    @api.depends('attendance_ids')
    def _compute_attendance_count(self):
        for session in self:
            session.attendance_count = len(session.attendance_ids)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.gym.session')
        return super().create(vals)

    def _check_coach_or_manager(self):
        for session in self:
            if not (self.env.user.has_group(
                    'sf_gym_fitness.group_sf_gym_manager') or
                    session.coach_id == self.env.user):
                raise UserError(_('Only the coach or a gym manager can '
                                  'update session statuses.'))

    def action_confirm(self):
        for session in self:
            if session.state != 'draft':
                raise UserError(_('Only draft sessions can be confirmed.'))
        self.state = 'confirmed'

    def action_cancel(self):
        for session in self:
            if session.state not in ('draft', 'confirmed'):
                raise UserError(_('Only draft or confirmed sessions can be '
                                  'cancelled.'))
        self.state = 'cancelled'

    def action_mark_in_progress(self):
        self._check_coach_or_manager()
        for session in self:
            if session.state != 'confirmed':
                raise UserError(_('Only confirmed sessions can be marked '
                                  'as in progress.'))
        self.state = 'in_progress'

    def action_mark_done(self):
        self._check_coach_or_manager()
        for session in self:
            if session.state != 'in_progress':
                raise UserError(_('Only in progress sessions can be marked '
                                  'as done.'))
        self.state = 'done'
