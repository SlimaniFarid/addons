# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.time.attendance.monthly'

    def action_refresh_business(self):
        """Pull employee tenure and status."""
        for rec in self:
            emp = getattr(rec, 'employee_id', False)
            if not emp:
                continue
            hire = emp.first_contract_date or False
            years = ''
            if hire:
                delta = (fields.Date.context_today(rec) - hire).days
                years = ', tenure {:.1f}y'.format(delta / 365.25)
            rec.message_post(body=_('{name} ({dept}){tenure}, '
                                    'active={act}.').format(
                name=emp.name,
                dept=emp.department_id.name or '-',
                tenure=years,
                act=emp.active))
        return True
