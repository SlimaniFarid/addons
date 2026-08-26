from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class SpaPackage(models.Model):
    _name = 'sf.spa.package'
    _description = 'Client Package'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sequence_code = 'sf.spa.package'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    package_template_id = fields.Many2one('sf.spa.service', string='Package Template', required=True, domain=[('is_package', '=', True)])
    sessions_total = fields.Integer(string='Total Sessions', compute='_compute_sessions_total', store=True)
    sessions_used = fields.Integer(string='Sessions Used', default=0, tracking=True)
    sessions_remaining = fields.Integer(string='Sessions Remaining', compute='_compute_sessions_remaining')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    expiry_date = fields.Date(string='Expiry Date', required=True, tracking=True)
    state = fields.Selection([
        ('sold', 'Sold'),
        ('active', 'Active'),
        ('partially_used', 'Partially Used'),
        ('exhausted', 'Exhausted'),
        ('expired', 'Expired'),
        ('refunded', 'Refunded'),
    ], string='State', default='sold', tracking=True)
    booking_ids = fields.One2many('sf.spa.booking', 'package_id', string='Bookings')
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)

    @api.depends('package_template_id')
    def _compute_sessions_total(self):
        for record in self:
            if record.package_template_id:
                record.sessions_total = sum(record.package_template_id.package_session_ids.mapped('quantity'))
            else:
                record.sessions_total = 0

    @api.depends('sessions_total', 'sessions_used')
    def _compute_sessions_remaining(self):
        for record in self:
            record.sessions_remaining = record.sessions_total - record.sessions_used

    def _consume_session(self):
        self.ensure_one()
        if self.state in ('exhausted', 'expired', 'refunded'):
            raise UserError(_('Cannot consume session from %s package.') % self.state)
        self.sessions_used += 1
        if self.sessions_used >= self.sessions_total:
            self.state = 'exhausted'
        elif self.sessions_used > 0:
            self.state = 'partially_used'
        else:
            self.state = 'active'

    def action_activate(self):
        for record in self:
            if record.state == 'sold':
                record.state = 'active'

    def action_expire(self):
        for record in self:
            if record.state not in ('exhausted', 'refunded'):
                record.state = 'expired'

    def action_refund(self):
        for record in self:
            if record.state in ('exhausted', 'refunded'):
                raise UserError(_('Cannot refund %s package.') % record.state)
            record.state = 'refunded'

    @api.constrains('sessions_used', 'sessions_total')
    def _check_sessions(self):
        for record in self:
            if record.sessions_used < 0:
                raise ValidationError(_('Sessions used cannot be negative.'))
            if record.sessions_used > record.sessions_total:
                raise ValidationError(_('Sessions used cannot exceed total sessions.'))

    @api.constrains('start_date', 'expiry_date')
    def _check_dates(self):
        for record in self:
            if record.expiry_date < record.start_date:
                raise ValidationError(_('Expiry date must be after start date.'))