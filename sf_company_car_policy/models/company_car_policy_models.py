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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.car.assignment'

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
