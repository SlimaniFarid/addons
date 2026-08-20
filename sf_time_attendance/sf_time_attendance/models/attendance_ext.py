# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AttendanceExt(models.Model):
    _inherit = 'hr.attendance'

    expected_shift_hours = fields.Float(string='Expected Hours',
                                        compute='_compute_time_fields',
                                        store=True)
    shift_overtime = fields.Float(string='Overtime vs Shift',
                                  compute='_compute_time_fields',
                                  store=True)
    late_minutes = fields.Integer(string='Late (minutes)',
                                  compute='_compute_time_fields',
                                  store=True)
    is_late = fields.Boolean(string='Late', compute='_compute_time_fields',
                             store=True)

    @api.depends('check_in', 'check_out', 'employee_id')
    def _compute_time_fields(self):
        for att in self:
            att.expected_shift_hours = 0.0
            att.shift_overtime = 0.0
            att.late_minutes = 0
            att.is_late = False
            if not att.check_in:
                continue
            worked = att.worked_hours or 0.0
            shift = self.env['sf.time.attendance.shift'].search([
                ('employee_id', '=', att.employee_id.id),
                ('day_of_week', '=', str(att.check_in.weekday())),
                ('active', '=', True),
            ], limit=1)
            if shift:
                att.expected_shift_hours = round(shift.expected_hours(), 2)
                att.shift_overtime = round(max(worked - att.expected_shift_hours,
                                               0.0), 2)
                late_secs = (att.check_in -
                             att.check_in.replace(
                                 hour=int(shift.start_time),
                                 minute=int((shift.start_time % 1) * 60)))
                att.late_minutes = int(max(late_secs.total_seconds() / 60, 0))
                att.is_late = att.late_minutes > 5