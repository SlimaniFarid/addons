# -*- coding: utf-8 -*-
"""Company Car Policy & Eligibility models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCarAssignment(models.Model):
    _name = 'sf.car.assignment'
    _description = 'Company Car Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    grade = fields.Char(string='Grade / Level')
    co2_gkm = fields.Integer(string='CO2 (g/km)')
    fuel_card_ref = fields.Char(string='Fuel Card Ref')
    contract_end = fields.Date(string='Contract End')
    eligible = fields.Boolean(string='Eligible', default=True)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('assigned', 'Assigned'),
        ('returned', 'Returned'),
        ], string='Status', default='assigned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.car.assignment') or 'NEW'
        return super().create(vals_list)

    def action_returned(self):
        self.write({'state': 'returned'})

