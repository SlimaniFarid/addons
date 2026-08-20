# -*- coding: utf-8 -*-
import re
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSalonCommission(models.Model):
    _name = 'sf.salon.commission'
    _description = 'Salon Commission'
    _order = 'period desc, id desc'

    _sql_constraints = [
        ('commission_staff_period_uniq', 'UNIQUE (staff_id, period, company_id)',
         'A commission already exists for this staff member and period.'),
    ]

    name = fields.Char(string='Name', required=True, copy=False)
    period = fields.Char(string='Period', required=True)
    staff_id = fields.Many2one('sf.salon.staff', string='Staff', required=True, ondelete='cascade')
    amount = fields.Monetary(string='Amount', compute='_compute_amount', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Computed'),
        ('paid', 'Paid'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @staticmethod
    def _split_period(period):
        if not period or not re.match(r'^\d{4}-\d{2}$', str(period)):
            raise UserError(_('Invalid period "%s". Expected the YYYY-MM format (e.g. 2026-08).') % period)
        year = int(period[:4])
        month = int(period[5:7])
        if month < 1 or month > 12:
            raise UserError(_('Invalid month in period "%s". Expected a value between 01 and 12.') % period)
        return year, month

    @classmethod
    def _period_range(cls, period):
        year, month = cls._split_period(period)
        start = datetime(year, month, 1)
        end = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
        return start, end

    @api.depends('staff_id', 'period', 'company_id')
    def _compute_amount(self):
        Appointment = self.env['sf.salon.appointment']
        for commission in self:
            try:
                start, end = self._period_range(commission.period)
            except UserError:
                commission.amount = 0.0
                continue
            grouped = Appointment.read_group(
                domain=[
                    ('staff_id', '=', commission.staff_id.id),
                    ('state', '=', 'done'),
                    ('package_id', '=', False),
                    ('company_id', '=', commission.company_id.id),
                    ('start_datetime', '>=', start),
                    ('start_datetime', '<', end),
                ],
                fields=['service_id'],
                groupby=['service_id'],
                lazy=False,
            )
            service_by_id = {s.id: s for s in self.env['sf.salon.service'].browse([
                row['service_id'][0] for row in grouped if row.get('service_id')
            ])}
            total = 0.0
            for row in grouped:
                if not row.get('service_id'):
                    continue
                service = service_by_id[row['service_id'][0]]
                rate = service.commission_rate
                if rate is False:
                    rate = commission.staff_id.commission_rate
                total += service.price * float(rate) * row['__count'] / 100.0
            commission.amount = total

    def _check_manager(self):
        if not self.env.user.has_group('sf_salon_beauty.group_sf_salon_manager'):
            raise UserError(_('Only a salon manager can perform this action.'))

    def action_compute(self):
        for commission in self:
            commission._compute_amount()
            commission.state = 'computed'

    def action_paid(self):
        self._check_manager()
        for commission in self:
            commission.state = 'paid'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.salon.commission')
            if vals.get('period'):
                self._split_period(vals['period'])
        return super().create(vals_list)

    def write(self, vals):
        if 'period' in vals:
            self._split_period(vals['period'])
        return super().write(vals)