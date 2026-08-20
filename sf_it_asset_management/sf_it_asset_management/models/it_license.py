# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ItLicense(models.Model):
    _name = 'sf.it.license'
    _description = 'IT Software License'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    vendor_id = fields.Many2one('res.partner', string='Publisher')
    seats = fields.Integer(string='Seats', default=1, required=True)
    unlimited = fields.Boolean(string='Unlimited Seats')
    used_seats = fields.Integer(string='Used Seats',
                                compute='_compute_used_seats', store=True)
    available_seats = fields.Integer(string='Available Seats',
                                     compute='_compute_used_seats',
                                     store=True)
    expiration_date = fields.Date(string='Expiration Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expiring', 'Expiring'),
        ('expired', 'Expired'),
        ('renewed', 'Renewed'),
    ], string='Status', default='draft', tracking=True)
    license_key = fields.Char(string='License Key')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    assignments = fields.One2many('sf.it.license.assignment',
                                  'license_id',
                                  string='Assignments')
    notes = fields.Text(string='Notes')

    @api.depends('assignments.state')
    def _compute_used_seats(self):
        for license in self:
            used = sum(1 for a in license.assignments
                       if a.state == 'active')
            license.used_seats = used
            if license.unlimited:
                license.available_seats = -1
            else:
                license.available_seats = license.seats - used

    @api.constrains('seats')
    def _check_seats(self):
        for license in self:
            if license.seats < 0:
                raise UserError(_('The number of seats cannot be negative.'))

    def action_activate(self):
        for license in self:
            if license.state != 'draft':
                raise UserError(_('Only draft licenses can be activated.'))
            license.state = 'active'

    def action_renew(self):
        view = self.env.ref('sf_it_asset_management.it_license_renew_wizard_form')
        return {
            'name': _('Renew License'),
            'type': 'ir.actions.act_window',
            'res_model': 'sf.it.license.renew.wizard',
            'view_mode': 'form',
            'view_id': view.id,
            'target': 'new',
            'context': {'default_license_id': self.id},
        }

    def _cron_check_expiration(self):
        today = fields.Date.today()
        from datetime import timedelta
        soon = today + timedelta(days=30)
        licenses = self.search([('state', 'in', ('active', 'expiring'))])
        for license in licenses:
            if not license.expiration_date:
                continue
            if license.expiration_date < today:
                license.state = 'expired'
            elif license.expiration_date <= soon:
                if license.state == 'active':
                    license.state = 'expiring'
                    license.activity_schedule(
                        'mail.mail_activity_data_todo',
                        _('License %s expires soon.') % license.name,
                        user_id=license.env.user.id)