# -*- coding: utf-8 -*-
from odoo import fields, models, _


class TimeAttendanceShift(models.Model):
    _name = 'sf.time.attendance.shift'
    _description = 'Employee Shift Pattern'
    _rec_name = 'employee_id'
    _order = 'employee_id, day_of_week'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    ], string='Day of Week', required=True)
    start_time = fields.Float(string='Start Time', required=True,
                              help="Shift start, e.g. 9.0 = 09:00")
    end_time = fields.Float(string='End Time', required=True,
                            help="Shift end, e.g. 17.0 = 17:00")
    lunch_break_hours = fields.Float(string='Lunch Break (hours)',
                                     default=1.0)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('shift_uniq', 'unique(employee_id, day_of_week)',
         'Only one shift per employee and weekday.'),
    ]

    def expected_hours(self):
        """Hours expected for this shift."""
        self.ensure_one()
        return max(self.end_time - self.start_time - self.lunch_break_hours,
                   0.0)