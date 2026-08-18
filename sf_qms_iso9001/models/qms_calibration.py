from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QMSCalibration(models.Model):
    _name = 'qms.calibration'
    _description = 'Equipment Calibration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'next_due_date'

    name = fields.Char(string='Equipment Name', required=True)
    code = fields.Char(string='Equipment Code', required=True, copy=False)
    company_id = fields.Many2one('res.company', default=lambda s: s.env.company)

    # Classification
    category = fields.Selection([
        ('measurement', 'Measurement Device'),
        ('test', 'Test Equipment'),
        ('inspection', 'Inspection Equipment'),
        ('monitoring', 'Monitoring Device'),
        ('safety', 'Safety Device'),
        ('other', 'Other'),
    ], string='Category', required=True)

    # Specifications
    manufacturer = fields.Char(string='Manufacturer')
    model = fields.Char(string='Model')
    serial_number = fields.Char(string='Serial Number')
    asset_number = fields.Char(string='Asset Number')
    location_id = fields.Many2one('stock.location', string='Location')
    department_id = fields.Many2one('hr.department', string='Department')

    # Calibration Specs
    calibration_frequency_months = fields.Integer(string='Frequency (Months)', default=12)
    calibration_method = fields.Text(string='Calibration Method / Procedure')
    accuracy_class = fields.Char(string='Accuracy Class')
    measurement_range = fields.Char(string='Measurement Range')
    tolerance = fields.Char(string='Tolerance / Uncertainty')

    # Status
    state = fields.Selection([
        ('active', 'Active'),
        ('due', 'Calibration Due'),
        ('overdue', 'Overdue'),
        ('in_calibration', 'In Calibration'),
        ('out_of_service', 'Out of Service'),
        ('disposed', 'Disposed'),
    ], string='Status', default='active', tracking=True)

    # Dates
    last_calibration_date = fields.Date(string='Last Calibration')
    next_due_date = fields.Date(string='Next Due Date', compute='_compute_next_due', store=True)
    calibration_due_soon = fields.Boolean(string='Due Soon', compute='_compute_due_soon')

    # Provider
    calibration_provider = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External Lab'),
    ], string='Provider', default='internal')
    external_lab_id = fields.Many2one('res.partner', string='External Lab',
        domain=[('is_company', '=', True)])

    # Records
    record_ids = fields.One2many('qms.calibration.record', 'equipment_id', string='Calibration Records')

    @api.depends('last_calibration_date', 'calibration_frequency_months')
    def _compute_next_due(self):
        for eq in self:
            if eq.last_calibration_date and eq.calibration_frequency_months:
                from dateutil.relativedelta import relativedelta
                eq.next_due_date = eq.last_calibration_date + relativedelta(months=eq.calibration_frequency_months)
            else:
                eq.next_due_date = False

    @api.depends('next_due_date')
    def _compute_due_soon(self):
        for eq in self:
            eq.calibration_due_soon = eq.next_due_date and eq.next_due_date <= fields.Date.today() + timedelta(days=30)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('qms.calibration') or 'CAL-%s' % self.env['ir.sequence'].next_by_code('qms.calibration')
        return super().create(vals_list)


class QMSCalibrationRecord(models.Model):
    _name = 'qms.calibration.record'
    _description = 'Calibration Record'
    _order = 'calibration_date desc'

    equipment_id = fields.Many2one('qms.calibration', string='Equipment', required=True, ondelete='cascade')
    calibration_date = fields.Date(string='Calibration Date', default=fields.Date.today, required=True)
    next_due_date = fields.Date(string='Next Due Date', required=True)

    # Results
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('adjusted', 'Adjusted & Pass'),
        ('out_of_tolerance', 'Out of Tolerance'),
    ], string='Result', required=True)

    as_found_data = fields.Text(string='As-Found Data')
    as_left_data = fields.Text(string='As-Left Data')
    uncertainty = fields.Char(string='Measurement Uncertainty')
    environmental_conditions = fields.Char(string='Environmental Conditions')

    # Provider
    performed_by_id = fields.Many2one('res.users', string='Performed By')
    external_lab_id = fields.Many2one('res.partner', string='External Lab')
    certificate_number = fields.Char(string='Certificate Number')
    certificate_attachment = fields.Many2one('ir.attachment', string='Certificate')

    # Traceability
    standard_used = fields.Char(string='Standard Used')
    standard_due_date = fields.Date(string='Standard Due Date')

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)

    approved_by_id = fields.Many2one('res.users', string='Approved By')
    approved_date = fields.Date(string='Approved Date')

    def action_approve(self):
        self.write({'state': 'approved', 'approved_by_id': self.env.user.id, 'approved_date': fields.Date.today()})
        # Update equipment next due date
        self.equipment_id.write({
            'last_calibration_date': self.calibration_date,
        })

    def action_reject(self):
        self.write({'state': 'rejected'})