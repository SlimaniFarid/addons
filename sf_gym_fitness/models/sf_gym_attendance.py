# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfGymAttendance(models.Model):
    _name = 'sf.gym.attendance'
    _description = 'Gym Attendance'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    session_id = fields.Many2one(
        'sf.gym.session', string='Session', ondelete='cascade',
        index=True, tracking=True, required=True)
    member_id = fields.Many2one(
        'sf.gym.member', string='Member', ondelete='restrict',
        index=True, tracking=True, required=True)
    state = fields.Selection([
        ('present', 'Present'),
    ], string='Status', default='present', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.gym.attendance')
        if vals.get('session_id'):
            session = self.env['sf.gym.session'].browse(
                vals['session_id'])
            if session.attendance_count >= session.capacity:
                raise UserError(_('The session is already full: maximum '
                                  '%s attendees.') % session.capacity)
        return super().create(vals)
