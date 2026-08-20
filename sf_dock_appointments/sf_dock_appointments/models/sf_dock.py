# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SfDock(models.Model):
    _name = 'sf.dock'
    _description = 'Dock'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.dock.appointments.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    dock_type = fields.Selection([
        ('receiving', 'Receiving'),
        ('shipping', 'Shipping'),
        ('both', 'Receiving & Shipping'),
    ], string='Dock Type', required=True, default='both')
    location_note = fields.Char(string='Location')
    is_active = fields.Boolean(string='Active', default=True)
    appointment_ids = fields.One2many('sf.dock.appointment', 'dock_id',
                                      string='Appointments')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company, index=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.dock')
        return super().create(vals_list)