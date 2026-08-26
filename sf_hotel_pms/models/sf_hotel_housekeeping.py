# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfHotelHousekeeping(models.Model):
    _name = 'sf.hotel.housekeeping'
    _description = 'Hotel Housekeeping'
    _order = 'date, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    room_id = fields.Many2one('sf.hotel.room', string='Room',
                              ondelete='cascade', required=True, index=True)
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today)
    task_type = fields.Selection([
        ('cleaning', 'Cleaning'),
        ('maintenance', 'Maintenance'),
    ], string='Task type', required=True, default='cleaning')
    assigned_to = fields.Many2one('res.users', string='Assigned to')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.hotel.housekeeping')
        return super().create(vals)

    def action_plan(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft tasks can be planned.'))
        self.state = 'planned'

    def action_done(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_hotel_pms.group_sf_hotel_manager'):
            raise UserError(_('Only hotel managers can close housekeeping '
                              'tasks.'))
        if self.state != 'planned':
            raise UserError(_('Only planned tasks can be marked as done.'))
        self.state = 'done'
