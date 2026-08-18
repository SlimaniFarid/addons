# -*- coding: utf-8 -*-
from odoo import fields, models, _


class PsaResource(models.Model):
    _name = 'sf.psa.resource'
    _description = 'PSA Resource'
    _rec_name = 'partner_id'
    _order = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    role = fields.Char(string='Role')
    hourly_rate = fields.Float(string='Hourly Rate', default=0.0)
    capacity_hours = fields.Float(string='Capacity Hours / Week',
                                  default=40.0)
    assignment_ids = fields.One2many('sf.psa.assignment', 'resource_id',
                                     string='Assignments')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('partner_uniq', 'unique(partner_id)', 'A resource must be unique.'),
    ]