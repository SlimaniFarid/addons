# -*- coding: utf-8 -*-
"""Employee Certificate Requests models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCertRequest(models.Model):
    _name = 'sf.cert.request'
    _description = 'Certificate Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    certificate_type = fields.Selection([
        ('work', 'Work Certificate'),
        ('salary', 'Salary Attestation'),
        ('employment', 'Employment Letter'),
        ('custom', 'Custom'),
        ], string='Type', required=True)
    request_date = fields.Date(string='Requested', default=fields.Date.today)
    delivered_date = fields.Date(string='Delivered')
    custom_text = fields.Text(string='Custom Text')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('prepared', 'Prepared'),
        ('delivered', 'Delivered'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.cert.request') or 'NEW'
        return super().create(vals_list)

    def action_prepared(self):
        self.write({'state': 'prepared'})

    def action_delivered(self):
        self.write({'state': 'delivered'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.cert.request'

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
