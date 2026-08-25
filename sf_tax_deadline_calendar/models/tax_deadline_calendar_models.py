# -*- coding: utf-8 -*-
"""Tax Deadline Calendar models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfTaxDeadline(models.Model):
    _name = 'sf.tax.deadline'
    _description = 'Tax Deadline'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    obligation = fields.Selection([
        ('vat', 'VAT Return'),
        ('corporate', 'Corporate Tax'),
        ('payroll', 'Payroll Taxes'),
        ('other', 'Other'),
        ], string='Obligation', required=True)
    due_date = fields.Date(string='Due Date', required=True)
    period_label = fields.Char(string='Period')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    amount_estimate = fields.Monetary(string='Estimated Amount')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('prepared', 'Prepared'),
        ('filed', 'Filed'),
        ('paid', 'Paid'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.tax.deadline') or 'NEW'
        return super().create(vals_list)

    def action_prepared(self):
        self.write({'state': 'prepared'})

    def action_filed(self):
        self.write({'state': 'filed'})

    def action_paid(self):
        self.write({'state': 'paid'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.tax.deadline'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

