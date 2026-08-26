# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSalonPackage(models.Model):
    _name = 'sf.salon.package'
    _description = 'Salon Package'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.salon.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='restrict')
    service_id = fields.Many2one('sf.salon.service', string='Service', required=True, ondelete='restrict')
    sessions_total = fields.Integer(string='Total Sessions', required=True, default=1)
    sessions_used = fields.Integer(string='Sessions Used', default=0, copy=False)
    sessions_left = fields.Integer(string='Sessions Left', compute='_compute_sessions_left', store=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('sold', 'Sold'),
        ('partially_used', 'Partially Used'),
        ('exhausted', 'Exhausted'),
        ('expired', 'Expired'),
        ('refunded', 'Refunded'),
    ], string='Status', default='sold', copy=False)
    expiration_date = fields.Date(string='Expiration Date')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('sessions_total', 'sessions_used')
    def _compute_sessions_left(self):
        for package in self:
            package.sessions_left = package.sessions_total - package.sessions_used

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.salon.package')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_salon_beauty.group_sf_salon_manager'):
            raise UserError(_('Only a salon manager can perform this action.'))

    @api.constrains('sessions_total', 'sessions_used')
    def _check_sessions(self):
        for package in self:
            if package.sessions_used < 0 or package.sessions_used > package.sessions_total:
                raise UserError(_('Sessions used cannot exceed the total sessions of the package.'))

    def _consume_session(self):
        self.ensure_one()
        if self.state in ('expired', 'refunded', 'exhausted'):
            raise UserError(_('This package is no longer usable.'))
        if self.expiration_date and self.expiration_date <= fields.Date.context_today(self):
            raise UserError(_('The package has reached its expiration date and cannot be used.'))
        if self.sessions_left <= 0:
            raise UserError(_('The package has no remaining sessions.'))
        self.sessions_used += 1
        if self.sessions_left <= 0:
            self.state = 'exhausted'
        else:
            self.state = 'partially_used'

    def action_refund(self):
        self.ensure_one()
        if self.state in ('exhausted', 'refunded'):
            raise UserError(_('An exhausted or refunded package cannot be refunded.'))
        self._check_manager()
        self.state = 'refunded'

    def _cron_daily_expirations(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            expiring = scoped.env['sf.salon.package'].search([
                ('state', 'in', ('sold', 'partially_used')),
            ]).filtered(lambda p: p.expiration_date and p.expiration_date <= today)
            for package in expiring:
                package.state = 'expired'
                package._sf_check_todo(
                    todo_type,
                    'Package %s has expired' % package.name,
                    'Reminder: the package has reached its expiration date.',
                )