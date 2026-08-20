# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfTravelPackage(models.Model):
    _name = 'sf.travel.package'
    _description = 'Travel Package'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, readonly=True, copy=False)
    destination = fields.Char(string='Destination', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    price_unit = fields.Monetary(string='Price', currency_field='currency_id', required=True)
    capacity = fields.Integer(string='Capacity', default=0)
    provider_ids = fields.Many2many('sf.travel.provider', string='Providers')
    reservation_ids = fields.One2many('sf.travel.reservation', 'package_id', string='Reservations')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('on_sale', 'On Sale'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.travel.package') or 'New'
        return super(SfTravelPackage, self).create(vals)

    def write(self, vals):
        if 'price_unit' in vals and not self.env.user.has_group('sf_travel_agency.group_sf_travel_agency_manager'):
            raise UserError(_('Only managers can modify package prices.'))
        return super(SfTravelPackage, self).write(vals)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise UserError(_('The package end date must be greater than or equal to its start date.'))

    @api.constrains('provider_ids')
    def _check_providers(self):
        for rec in self:
            providers = rec.with_context(active_test=False).provider_ids
            if any(provider.state == 'archived' for provider in providers):
                raise UserError(_('An archived provider cannot be added to a package.'))

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_on_sale(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError(_('Only confirmed packages can be put on sale.'))
            rec.state = 'on_sale'

    def action_close(self):
        for rec in self:
            rec.state = 'closed'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def _cron_departure_and_unpaid_alerts(self):
        todos = self.env.ref('mail.mail_activity_data_todo')
        reminder_days = int(self.env['ir.config_parameter'].sudo().get_param('sf_travel_agency.reminder_days', '7') or 7)
        for company in self.env['res.company'].search([]):
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            date_to = today + timedelta(days=reminder_days)
            packages = scoped.env['sf.travel.package'].search([
                ('start_date', '>=', today),
                ('start_date', '<=', date_to),
            ])
            for package in packages:
                subject = 'Departure soon: %s' % package.name
                existing = package.activity_ids.filtered(lambda act: act.activity_type_id == todos and act.summary == subject and not act.done)
                if not existing:
                    package.activity_schedule(
                        activity_type_id=todos.id,
                        summary=subject,
                        note=_('The package %s departs on %s.') % (package.name, package.start_date),
                    )
            cutoff = today - timedelta(hours=48)
            reservations = scoped.env['sf.travel.reservation'].search([
                ('state', '=', 'confirmed'),
                ('booking_date', '<=', cutoff),
            ])
            for reservation in reservations:
                subject = 'Unpaid reservation: %s' % reservation.name
                existing = reservation.activity_ids.filtered(lambda act: act.activity_type_id == todos and act.summary == subject and not act.done)
                if not existing:
                    reservation.activity_schedule(
                        activity_type_id=todos.id,
                        summary=subject,
                        note=_('The reservation %s has been confirmed and is unpaid for more than 48 hours.') % reservation.name,
                    )
