from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class SpaMembership(models.Model):
    _name = 'sf.spa.membership'
    _description = 'Wellness Membership'
    _inherit = ['sf.spa.sequence.mixin', 'sf.spa.company.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _sequence_code = 'sf.spa.membership'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Holder', required=True, tracking=True)
    membership_type = fields.Selection([
        ('solo', 'Solo'),
        ('duo', 'Duo'),
        ('family', 'Family'),
        ('corporate', 'Corporate'),
    ], string='Type', required=True, default='solo', tracking=True)
    access_level = fields.Selection([
        ('full_facilities', 'Full Facilities'),
        ('limited_facilities', 'Limited Facilities'),
    ], string='Access Level', default='full_facilities')
    monthly_credits = fields.Float(string='Monthly Credits', default=0.0, tracking=True)
    credits_available = fields.Float(string='Available Credits', compute='_compute_credits_available')
    price_monthly = fields.Monetary(string='Monthly Price', currency_field='currency_id')
    price_yearly = fields.Monetary(string='Yearly Price', currency_field='currency_id')
    billing_cycle = fields.Selection([
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string='Billing Cycle', default='monthly')
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date', tracking=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ], string='State', default='active', tracking=True)
    beneficiary_ids = fields.One2many('sf.spa.membership.beneficiary', 'membership_id', string='Beneficiaries')
    invoice_ids = fields.One2many('account.move', 'membership_id', string='Invoices')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    @api.depends('monthly_credits', 'beneficiary_ids')
    def _compute_credits_available(self):
        for record in self:
            used = sum(record.beneficiary_ids.mapped('credits_used'))
            record.credits_available = record.monthly_credits - used

    def action_activate(self):
        for record in self:
            if record.state in ('suspended', 'cancelled', 'expired'):
                record.state = 'active'

    def action_suspend(self):
        for record in self:
            if record.state == 'active':
                record.state = 'suspended'

    def action_cancel(self):
        for record in self:
            if record.state in ('cancelled', 'expired'):
                continue
            record.state = 'cancelled'

    def action_renew(self):
        for record in self:
            if record.billing_cycle == 'monthly':
                record.end_date = (record.end_date or fields.Date.today()) + relativedelta(months=1)
            else:
                record.end_date = (record.end_date or fields.Date.today()) + relativedelta(years=1)
            record.state = 'active'

    @api.model
    def _cron_reset_credits(self):
        memberships = self.search([('state', '=', 'active')])
        for membership in memberships:
            membership.beneficiary_ids.write({'credits_used': 0.0})

    @api.constrains('price_monthly', 'price_yearly')
    def _check_prices(self):
        for record in self:
            if record.price_monthly < 0 or record.price_yearly < 0:
                raise ValidationError(_('Prices cannot be negative.'))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.end_date < record.start_date:
                raise ValidationError(_('End date must be after start date.'))


class SpaMembershipBeneficiary(models.Model):
    _name = 'sf.spa.membership.beneficiary'
    _description = 'Membership Beneficiary'
    _inherit = ['sf.spa.company.mixin']

    membership_id = fields.Many2one('sf.spa.membership', string='Membership', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Beneficiary', required=True)
    relationship = fields.Selection([
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('employee', 'Employee'),
    ], string='Relationship', required=True)
    access_level = fields.Selection([
        ('full_facilities', 'Full Facilities'),
        ('limited_facilities', 'Limited Facilities'),
    ], string='Access Level', default='full_facilities')
    credits_used = fields.Float(string='Credits Used', default=0.0)

    _sql_constraints = [
        ('unique_beneficiary', 'unique(membership_id, partner_id)', 'A partner can only be beneficiary once per membership.'),
    ]