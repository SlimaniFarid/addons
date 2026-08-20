# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrecheAttendance(models.Model):
    _name = 'sf.creche.attendance'
    _description = 'Creche Attendance'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Attendance', required=True, index=True)
    child_id = fields.Many2one('sf.creche.child', string='Child',
                               required=True, ondelete='restrict',
                               index=True)
    date = fields.Date(string='Date', default=fields.Date.context_today,
                       required=True, index=True)
    arrival_time = fields.Float(string='Arrival time')
    departure_time = fields.Float(string='Departure time')
    hours = fields.Float(string='Hours', compute='_compute_hours', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('arrival_time', 'departure_time')
    def _compute_hours(self):
        for att in self:
            if att.arrival_time and att.departure_time:
                att.hours = att.departure_time - att.arrival_time
            else:
                att.hours = 0.0

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.creche.attendance')
        return super().create(vals)

    def _get_room(self):
        self.ensure_one()
        enrollment = self.env['sf.creche.enrollment'].search([
            ('child_id', '=', self.child_id.id),
            ('state', '=', 'active'),
        ], order='id desc', limit=1)
        return enrollment.room_id

    def action_done(self):
        for att in self:
            room = att._get_room()
            if room:
                present = self.search([
                    ('date', '=', att.date),
                    ('state', '=', 'done'),
                ])
                count = 1
                for other in present:
                    if other._get_room() == room:
                        count += 1
                if count > room.capacity:
                    raise UserError(
                        _('Room capacity exceeded: %s children present in '
                          '%s (capacity %s).') % (count, room.name,
                                                  room.capacity))
            att.state = 'done'
