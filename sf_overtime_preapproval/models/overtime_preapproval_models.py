# -*- coding: utf-8 -*-
"""Overtime Pre-Approval models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfOvertimeRequest(models.Model):
    _name = 'sf.overtime.request'
    _description = 'Overtime Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date = fields.Date(string='Overtime Date', required=True)
    estimated_hours = fields.Float(string='Estimated Hours')
    actual_hours = fields.Float(string='Actual Hours')
    project_ref = fields.Char(string='Project / Reason', required=True)
    approver_id = fields.Many2one('res.users', string='Approved By')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('pre_approved', 'Pre-Approved'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.overtime.request') or 'NEW'
        return super().create(vals_list)

    def action_pre_approved(self):
        self.write({'state': 'pre_approved'})

    def action_validated(self):
        self.write({'state': 'validated'})

    def action_rejected(self):
        self.write({'state': 'rejected'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.overtime.request'

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
