# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class SfEventSession(models.Model):
    _name = 'sf.event.session'
    _description = 'Event Session'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.events.activity.mixin']
    _order = 'start_datetime asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    event_id = fields.Many2one('sf.event', string='Event', required=True, ondelete='cascade')
    start_datetime = fields.Datetime(string='Start', required=True)
    end_datetime = fields.Datetime(string='End', required=True)
    room = fields.Char(string='Room')
    speaker_ids = fields.Many2many('res.partner', string='Speakers')
    capacity = fields.Integer(string='Capacity')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.event.session')
        return super().create(vals_list)

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft sessions can be confirmed.'))
        if self.event_id.state == 'cancelled':
            raise UserError(_('A session cannot be confirmed when its event is cancelled.'))
        self.state = 'confirmed'

    def action_done(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed sessions can be marked as done.'))
        self.state = 'done'