# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CrecheRoom(models.Model):
    _name = 'sf.creche.room'
    _description = 'Creche Room'
    _order = 'name'

    name = fields.Char(string='Room', required=True, index=True)
    capacity = fields.Integer(string='Capacity', required=True)
    educator_ids = fields.Many2many('res.users', string='Educators')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True)
    enrollment_ids = fields.One2many('sf.creche.enrollment', 'room_id',
                                     string='Enrollments')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.creche.room')
        return super().create(vals)

    def action_done(self):
        self.ensure_one()
        self.state = 'done'
