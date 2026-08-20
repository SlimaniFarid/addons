# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrecheBilling(models.Model):
    _name = 'sf.creche.billing'
    _description = 'Creche Billing'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Billing', required=True, index=True)
    child_id = fields.Many2one('sf.creche.child', string='Child',
                               required=True, ondelete='restrict',
                               index=True)
    month = fields.Char(string='Month', required=True)
    hours = fields.Float(string='Hours', compute='_compute_hours', store=True)
    hourly_rate = fields.Float(string='Hourly rate')
    amount = fields.Float(string='Amount', compute='_compute_amount',
                          store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('paid', 'Paid'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('child_id', 'month')
    def _compute_hours(self):
        Attendance = self.env['sf.creche.attendance']
        for bill in self:
            if not bill.child_id or not bill.month:
                bill.hours = 0.0
                continue
            try:
                start = datetime.strptime(bill.month, '%Y-%m').date()
            except ValueError:
                bill.hours = 0.0
                continue
            if start.month == 12:
                end = start.replace(year=start.year + 1, month=1, day=1)
            else:
                end = start.replace(month=start.month + 1, day=1)
            attendances = Attendance.search([
                ('child_id', '=', bill.child_id.id),
                ('date', '>=', start),
                ('date', '<', end),
                ('state', '=', 'done'),
            ])
            bill.hours = sum(attendances.mapped('hours'))

    @api.depends('hours', 'hourly_rate')
    def _compute_amount(self):
        for bill in self:
            bill.amount = bill.hours * bill.hourly_rate

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.creche.billing')
        if not vals.get('hourly_rate'):
            company = self.env['res.company'].browse(
                vals.get('company_id') or self.env.company.id)
            vals['hourly_rate'] = company.sf_creche_hourly_rate
        return super().create(vals)

    def action_issue(self):
        self.ensure_one()
        if not self.user_has_groups('sf_creche.group_sf_creche_manager'):
            raise UserError(_('Only a Creche Manager can issue an invoice.'))
        self.state = 'issued'

    def action_pay(self):
        self.ensure_one()
        if not self.user_has_groups('sf_creche.group_sf_creche_manager'):
            raise UserError(_('Only a Creche Manager can mark an invoice '
                              'as paid.'))
        self.state = 'paid'
