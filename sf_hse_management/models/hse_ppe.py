# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HsePpe(models.Model):
    _name = 'sf.hse.ppe'
    _description = 'HSE PPE'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    ppe_type = fields.Selection([
        ('helmet', 'Helmet'),
        ('gloves', 'Gloves'),
        ('goggles', 'Goggles'),
        ('mask', 'Mask'),
        ('harness', 'Harness'),
        ('hearing', 'Hearing Protection'),
        ('boots', 'Safety Boots'),
        ('other', 'Other'),
    ], string='Type', default='other')
    serial_number = fields.Char(string='Serial Number')
    employee_id = fields.Many2one('hr.employee', string='Assigned To')
    assignment_date = fields.Date(string='Assignment Date')
    expiry_date = fields.Date(string='Expiry Date')
    state = fields.Selection([
        ('in_stock', 'In Stock'),
        ('assigned', 'Assigned'),
        ('expired', 'Expired'),
    ], string='Status', compute='_compute_state', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)

    @api.depends('employee_id', 'expiry_date')
    def _compute_state(self):
        for ppe in self:
            if ppe.expiry_date and ppe.expiry_date < fields.Date.today():
                ppe.state = 'expired'
            elif ppe.employee_id:
                ppe.state = 'assigned'
            else:
                ppe.state = 'in_stock'