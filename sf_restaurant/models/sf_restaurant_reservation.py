# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class SfRestaurantReservation(models.Model):
    _name = 'sf.restaurant.reservation'
    _description = 'Restaurant Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.restaurant.activity.mixin']
    _order = 'reservation_date desc, start_time'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='set null')
    contact_name = fields.Char(string='Contact Name')
    phone = fields.Char(string='Phone')
    reservation_date = fields.Date(string='Reservation Date', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    guests = fields.Integer(string='Guests', required=True)
    table_ids = fields.Many2many('sf.restaurant.table', string='Tables')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.restaurant.reservation')
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        if vals.get('guests') or vals.get('table_ids') or vals.get('start_time'):
            for r in self:
                if r.state in ('confirmed', 'seated'):
                    r._check_capacity()
        return res

    def _check_capacity(self):
        self.ensure_one()
        if not self.table_ids:
            raise UserError(_('At least one table must be selected for the reservation.'))
        active = self.env['sf.restaurant.reservation'].search([
            ('reservation_date', '=', self.reservation_date),
            ('start_time', '=', self.start_time),
            ('state', 'in', ('confirmed', 'seated')),
            ('id', '!=', self.id),
        ])
        active_guests = sum(active.mapped('guests'))
        capacity = sum(self.table_ids.mapped('seats'))
        if self.guests + active_guests > capacity:
            raise UserError(_('Insufficient capacity for this time slot.'))

    def _check_manager(self):
        if not self.env.user.has_group('sf_restaurant.group_sf_restaurant_manager'):
            raise UserError(_('Only a restaurant manager can perform this action.'))

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft reservations can be confirmed.'))
        self._check_capacity()
        self.state = 'confirmed'
        self.table_ids.write({'state': 'reserved'})

    def action_seat(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed reservations can be seated.'))
        self.state = 'seated'
        self.table_ids.write({'state': 'occupied'})

    def action_done(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'seated'):
            raise UserError(_('Only confirmed or seated reservations can be marked as done.'))
        self.state = 'done'
        for table in self.table_ids:
            if not table.current_order_id or table.current_order_id.state == 'closed':
                table.state = 'free'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'seated':
            raise UserError(_('A seated reservation cannot be cancelled.'))
        if self.state == 'confirmed':
            self._check_manager()
        for table in self.table_ids:
            if table.state == 'reserved':
                table.state = 'free'
        self.state = 'cancelled'

    def _cron_daily_alerts(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            reservations = scoped.env['sf.restaurant.reservation'].search([
                ('state', '=', 'confirmed'),
                ('reservation_date', '=', today),
            ])
            for reservation in reservations:
                reservation._sf_check_todo(
                    todo_type,
                    'Reservation %s today at %s' % (reservation.name, reservation.start_time),
                    'Reminder: the reservation is scheduled for today.',
                )
            occupied = scoped.env['sf.restaurant.table'].search([
                ('state', '=', 'occupied'),
            ])
            avg_hours = float(scoped.env['ir.config_parameter'].sudo().get_param(
                'sf_restaurant.avg_service_hours', '1.5'
            ))
            for table in occupied:
                if table.current_order_id and table.current_order_id.order_date < today:
                    table._sf_check_todo(
                        todo_type,
                        'Table %s occupied beyond average duration' % table.name,
                        'Reminder: the table has been occupied for more than %s hours.' % avg_hours,
                    )