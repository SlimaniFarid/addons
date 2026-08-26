# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfHotelExtra(models.Model):
    _name = 'sf.hotel.extra'
    _description = 'Hotel Extra'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    reservation_id = fields.Many2one('sf.hotel.reservation',
                                     string='Reservation',
                                     ondelete='cascade', required=True,
                                     index=True)
    description = fields.Char(string='Description')
    amount = fields.Float(string='Amount')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('charged', 'Charged'),
    ], string='Status', default='draft', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.hotel.extra')
        return super().create(vals)

    def action_charge(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_hotel_pms.group_sf_hotel_manager'):
            raise UserError(_('Only hotel managers can charge extras.'))
        if self.state != 'draft':
            raise UserError(_('Only draft extras can be charged.'))
        self.state = 'charged'
