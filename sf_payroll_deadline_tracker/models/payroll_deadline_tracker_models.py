# -*- coding: utf-8 -*-
"""Payroll Deadline Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPayrollDeadline(models.Model):
    _name = 'sf.payroll.deadline'
    _description = 'Payroll Deadline'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period_month = fields.Date(string='Payroll Period', required=True)
    input_cutoff = fields.Date(string='Input Cutoff', required=True)
    processing_date = fields.Date(string='Processing Date')
    payment_date = fields.Date(string='Payment Date', required=True)
    declaration_date = fields.Date(string='Declaration Date')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('inputs_locked', 'Inputs Locked'),
        ('processed', 'Processed'),
        ('paid', 'Paid'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.payroll.deadline') or 'NEW'
        return super().create(vals_list)

    def action_inputs_locked(self):
        self.write({'state': 'inputs_locked'})

    def action_processed(self):
        self.write({'state': 'processed'})

    def action_paid(self):
        self.write({'state': 'paid'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.payroll.deadline'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.payroll.deadline'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
