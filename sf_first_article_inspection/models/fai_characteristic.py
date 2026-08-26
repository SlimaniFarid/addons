# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FAICharacteristic(models.Model):
    _name = 'sf.fai.characteristic'
    _description = 'FAI Characteristic'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    report_id = fields.Many2one('sf.fai.report', string='FAI Report', required=True, ondelete='cascade')
    characteristic_number = fields.Char(string='Char #', required=True)
    balloon_number = fields.Char(string='Balloon #')
    characteristic_name = fields.Char(string='Characteristic Name')
    specification = fields.Char(string='Specification')
    nominal = fields.Float(string='Nominal Value')
    tolerance_plus = fields.Float(string='Upper Tolerance')
    tolerance_minus = fields.Float(string='Lower Tolerance')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    inspection_method = fields.Selection([
        ('cmm', 'CMM'),
        ('manual', 'Manual (Calipers/Micrometer)'),
        ('vision', 'Vision System'),
        ('gage', 'Functional Gage'),
        ('other', 'Other'),
    ], string='Inspection Method', default='manual')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment Used')
    sample_size = fields.Integer(string='Sample Size', default=1)
    measured_values = fields.Text(string='Measured Values (one per line)')
    upper_limit = fields.Float(string='Upper Limit', compute='_compute_limits', store=True)
    lower_limit = fields.Float(string='Lower Limit', compute='_compute_limits', store=True)
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('not_measured', 'Not Measured'),
    ], string='Result', default='not_measured')
    notes = fields.Text(string='Notes')
    nonconformance_id = fields.Many2one('sf.fai.nonconformance', string='Linked Non-conformance')

    @api.onchange('nominal', 'tolerance_plus', 'tolerance_minus')
    def _onchange_tolerance(self):
        # Update upper/lower limit display or validation
        for rec in self:
            if rec.nominal is not None and rec.tolerance_plus is not None and rec.tolerance_minus is not None:
                rec.upper_limit = rec.nominal + rec.tolerance_plus
                rec.lower_limit = rec.nominal - rec.tolerance_minus

    @api.depends('nominal', 'tolerance_plus', 'tolerance_minus')
    def _compute_limits(self):
        for rec in self:
            if rec.nominal is not None and rec.tolerance_plus is not None and rec.tolerance_minus is not None:
                rec.upper_limit = rec.nominal + rec.tolerance_plus
                rec.lower_limit = rec.nominal - rec.tolerance_minus
            else:
                rec.upper_limit = 0.0
                rec.lower_limit = 0.0