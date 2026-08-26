# -*- coding: utf-8 -*-
"""Out-of-Office & Backup Calendar models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfOooPeriod(models.Model):
    _name = 'sf.ooo.period'
    _description = 'OOO Period'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To', required=True)
    backup_id = fields.Many2one('hr.employee', string='Backup Person')
    handover_note = fields.Text(string='Handover Notes')
    reachable = fields.Boolean(string='Reachable in Emergency')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.ooo.period') or 'NEW'
        return super().create(vals_list)

    def action_active(self):
        self.write({'state': 'active'})

    def action_completed(self):
        self.write({'state': 'completed'})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.ooo.period'

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
