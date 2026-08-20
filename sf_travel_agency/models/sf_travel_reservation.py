# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfTravelReservation(models.Model):
    _name = 'sf.travel.reservation'
    _description = 'Travel Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'booking_date desc, id desc'

    name = fields.Char(string='Name', required=True, readonly=True, copy=False)
    package_id = fields.Many2one('sf.travel.package', string='Package', required=True, ondelete='cascade', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='restrict')
    traveler_name = fields.Char(string='Traveler Name')
    traveler_email = fields.Char(string='Traveler Email')
    pax = fields.Integer(string='Travelers', required=True, default=1)
    price_unit = fields.Monetary(string='Price', currency_field='currency_id', required=True)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today, required=True)
    cost = fields.Monetary(string='Cost', currency_field='currency_id', compute='_compute_cost', store=True)
    commission = fields.Monetary(string='Commission', currency_field='currency_id', compute='_compute_commission', store=True)
    margin = fields.Monetary(string='Margin', currency_field='currency_id', compute='_compute_margin', store=True)
    cost_ids = fields.One2many('sf.travel.provider.cost', 'reservation_id', string='Provider Costs')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('cost_ids', 'cost_ids.amount')
    def _compute_cost(self):
        for rec in self:
            rec.cost = sum(rec.cost_ids.mapped('amount'))

    @api.depends('price_unit')
    def _compute_commission(self):
        rate = float(self.env['ir.config_parameter'].sudo().get_param('sf_travel_agency.commission_rate', '10.0') or 10.0)
        for rec in self:
            rec.commission = rec.price_unit * rate / 100.0

    @api.depends('price_unit', 'cost')
    def _compute_margin(self):
        for rec in self:
            rec.margin = rec.price_unit - rec.cost

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.travel.reservation') or 'New'
        return super(SfTravelReservation, self).create(vals)

    @api.constrains('package_id', 'pax', 'state')
    def _check_capacity(self):
        for rec in self:
            if rec.state not in ('confirmed', 'paid'):
                continue
            if not rec.package_id or not rec.package_id.capacity:
                continue
            domain = [
                ('package_id', '=', rec.package_id.id),
                ('state', 'in', ('confirmed', 'paid')),
            ]
            if rec.id:
                domain.append(('id', '!=', rec.id))
            booked = sum(self.search(domain).mapped('pax'))
            if booked + rec.pax > rec.package_id.capacity:
                raise UserError(_('Package capacity reached.'))

    def action_confirm(self):
        for rec in self:
            if rec.package_id.state in ('closed', 'cancelled'):
                raise UserError(_('Reservation cannot be confirmed on a %s package.') % rec.package_id.state)
            if rec.state == 'cancelled':
                raise UserError(_('A cancelled reservation cannot be confirmed.'))
            rec.state = 'confirmed'
            if rec.partner_id:
                rec.message_subscribe(partner_ids=[rec.partner_id.id])
            todos = self.env.ref('mail.mail_activity_data_todo')
            rec.activity_schedule(
                activity_type_id=todos.id,
                summary=_('Reservation confirmation: %s') % rec.name,
                note=_('The reservation %s has been confirmed and must be tracked until completion.') % rec.name,
            )

    def action_paid(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError(_('Only confirmed reservations can be marked as paid.'))
            rec.state = 'paid'

    def action_completed(self):
        for rec in self:
            if rec.state != 'paid':
                raise UserError(_('Only paid reservations can be marked as completed.'))
            rec.state = 'completed'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'completed':
                raise UserError(_('A completed reservation cannot be cancelled.'))
            if rec.state == 'paid' and not self.env.user.has_group('sf_travel_agency.group_sf_travel_agency_manager'):
                raise UserError(_('Only managers can cancel a paid reservation.'))
            rec.state = 'cancelled'
