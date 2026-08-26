# -*- coding: utf-8 -*-
"""Telecom lines and invoice audits."""
from odoo import api, fields, models, _


class SfTelecomLine(models.Model):
    _name = 'sf.telecom.line'
    _description = 'Telecom Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Label', required=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    employee_id = fields.Many2one('hr.employee', string='Assigned To')
    department = fields.Char(string='Department')
    provider = fields.Char(string='Provider', required=True)
    phone_number = fields.Char(string='Number')
    line_type = fields.Selection([
        ('mobile', 'Mobile'), ('data', 'Data Plan'),
        ('landline', 'Landline'), ('internet', 'Internet Access')],
        required=True, default='mobile')
    monthly_cost = fields.Monetary(string='Monthly Plan Cost', required=True)
    contract_start = fields.Date(string='Contract Start')
    contract_end = fields.Date(string='Contract End')
    contract_ending_soon = fields.Boolean(
        string='Contract Ending (30d)', compute='_compute_ending')
    active = fields.Boolean(default=True)

    def _compute_ending(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.contract_ending_soon = bool(
                rec.contract_end and 0 <= (rec.contract_end - today).days <= 30)


class SfTelecomAudit(models.Model):
    _name = 'sf.telecom.audit'
    _description = 'Telecom Invoice Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'period_month desc'

    name = fields.Char(string='Audit', required=True, copy=False,
                       readonly=True, default='New')
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    provider = fields.Char(string='Provider', required=True)
    period_month = fields.Date(string='Invoice Month', required=True,
                               default=fields.Date.today)
    expected_cost = fields.Float(string='Expected (active lines)',
                                 readonly=True)
    invoiced_amount = fields.Float(string='Invoiced Amount', required=True)
    variance = fields.Float(string='Variance', compute='_compute_variance',
                            store=True)
    variance_percent = fields.Float(string='Variance %',
                                    compute='_compute_variance', store=True)
    tolerance_percent = fields.Float(string='Tolerance %', default=5.0)
    alert = fields.Boolean(string='Variance Alert',
                           compute='_compute_variance', store=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Reviewed')],
                             default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.telecom.audit') or 'TEL-NEW'
        return super().create(vals_list)

    @api.depends('invoiced_amount', 'expected_cost')
    def _compute_variance(self):
        for rec in self:
            rec.variance = rec.invoiced_amount - rec.expected_cost
            rec.variance_percent = (rec.variance / rec.expected_cost * 100.0
                                    if rec.expected_cost else 0.0)
            rec.alert = abs(rec.variance_percent) > rec.tolerance_percent

    def action_compute_expected(self):
        for rec in self:
            lines = self.env['sf.telecom.line'].search([
                ('provider', '=', rec.provider),
                ('company_id', '=', rec.company_id.id),
                ('active', '=', True)])
            rec.expected_cost = sum(lines.mapped('monthly_cost'))

    def action_mark_reviewed(self):
        self.write({'state': 'done'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.telecom.line'

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
