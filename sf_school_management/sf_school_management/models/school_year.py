# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SchoolYear(models.Model):
    _name = 'sf.school.year'
    _description = 'School Year'
    _order = 'date_from desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Year', required=True, index=True)
    date_from = fields.Date(string='Start date')
    date_to = fields.Date(string='End date')
    state = fields.Selection([
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='active', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.year')
        return super().create(vals)

    def action_close_year(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_('Only active years can be closed.'))
        self.state = 'closed'

    def action_reopen_year(self):
        self.ensure_one()
        if self.state != 'closed':
            raise UserError(_('Only closed years can be reopened.'))
        self.state = 'active'