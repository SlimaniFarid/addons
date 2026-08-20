# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfStaffingTimesheet(models.Model):
    _name = 'sf.staffing.timesheet'
    _description = 'Staffing Timesheet'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.staffing.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    mission_id = fields.Many2one('sf.staffing.mission', string='Mission', required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    hours = fields.Float(string='Hours', required=True)
    hourly_rate = fields.Monetary(string='Hourly Rate', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    amount = fields.Monetary(
        string='Amount',
        compute='_compute_amount',
        store=True,
        currency_field='currency_id',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    invoiced = fields.Boolean(string='Invoiced', default=False, copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('hours', 'hourly_rate')
    def _compute_amount(self):
        for timesheet in self:
            timesheet.amount = timesheet.hours * timesheet.hourly_rate

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.staffing.timesheet')
            if not vals.get('hourly_rate') and vals.get('mission_id'):
                vals['hourly_rate'] = self.env['sf.staffing.mission'].browse(vals['mission_id']).hourly_rate
            if vals.get('mission_id') and not vals.get('company_id'):
                vals['company_id'] = self.env['sf.staffing.mission'].browse(vals['mission_id']).company_id.id
        return super().create(vals_list)

    @api.constrains('hours')
    def _check_hours(self):
        for timesheet in self:
            if timesheet.hours <= 0:
                raise UserError(_('Timesheet hours must be strictly positive.'))
            if timesheet.hours > 24:
                raise UserError(_('Timesheet hours cannot exceed 24.'))

    def write(self, vals):
        if vals.get('state') == 'cancelled':
            for timesheet in self:
                if timesheet.mission_id.state == 'done':
                    raise UserError(_('A timesheet cannot be cancelled after the mission has been completed.'))
        return super().write(vals)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})