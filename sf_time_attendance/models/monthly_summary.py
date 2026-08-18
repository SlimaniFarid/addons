# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TimeAttendanceMonthlySummary(models.Model):
    _name = 'sf.time.attendance.monthly'
    _description = 'Monthly Attendance Summary'
    _rec_name = 'employee_id'
    _order = 'month desc'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    month = fields.Date(string='Month', required=True,
                        help="First day of the month.")
    worked_hours = fields.Float(string='Worked Hours', compute='_compute')
    expected_shift_hours = fields.Float(string='Expected Hours',
                                        compute='_compute')
    overtime_hours = fields.Float(string='Overtime Hours', compute='_compute')
    late_days = fields.Integer(string='Late Days', compute='_compute')

    @api.depends('employee_id', 'month')
    def _compute(self):
        for rec in self:
            start = rec.month
            end = start + fields.Date.relativedelta(months=1)
            atts = self.env['hr.attendance'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('check_in', '>=', start),
                ('check_in', '<', end),
            ])
            rec.worked_hours = round(sum(atts.mapped('worked_hours')), 2)
            rec.expected_shift_hours = round(
                sum(atts.mapped('expected_shift_hours')), 2)
            rec.overtime_hours = round(sum(atts.mapped('shift_overtime')), 2)
            rec.late_days = len(atts.filtered(lambda a: a.is_late))

    def action_generate_month(self):
        """Generate or update monthly summaries from attendance."""
        for rec in self:
            rec._compute()
        return True

    @api.model
    def action_generate_all_monthly(self):
        """Generate a summary for every employee with attendance."""
        employees = self.env['hr.employee'].search([])
        today = fields.Date.today()
        month = today.replace(day=1)
        for employee in employees:
            atts = self.env['hr.attendance'].search_count([
                ('employee_id', '=', employee.id),
                ('check_in', '>=', month),
            ])
            if not atts:
                continue
            rec = self.search([
                ('employee_id', '=', employee.id),
                ('month', '=', month),
            ], limit=1)
            vals = {'employee_id': employee.id, 'month': month}
            if rec:
                rec.write(vals)
            else:
                self.create(vals)
        return True