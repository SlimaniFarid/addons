from odoo import api, fields, models
from odoo.exceptions import UserError


class PortalSubscriptionMgmt(models.Model):
    _name = 'portal.subscription.mgmt'
    _description = 'Portal Subscription Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'partner_id, id'

    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda s: s.env.company)

    # Native subscription definition (replaces Enterprise sale.subscription)
    product_id = fields.Many2one(
        'product.product', string='Subscription Product', required=True,
        domain=[('recurring_invoice', '=', True)])
    quantity = fields.Float(string='Quantity', default=1.0)
    recurring_monthly_amount = fields.Monetary(
        string='Monthly Amount', currency_field='currency_id',
        compute='_compute_recurring_monthly_amount', store=True,
        readonly=False)
    currency_id = fields.Many2one(related='company_id.currency_id')
    next_invoice_date = fields.Date(string='Next Invoice Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)

    # Portal-specific settings
    allow_upgrade = fields.Boolean(string='Allow Upgrade', default=True)
    allow_downgrade = fields.Boolean(string='Allow Downgrade', default=True)
    allow_cancel = fields.Boolean(string='Allow Cancel', default=True)
    allow_pause = fields.Boolean(string='Allow Pause', default=False)

    # Payment method management (Community: no payment.token on file,
    # customer pays per invoice through standard /payment/pay flow)
    allow_payment_update = fields.Boolean(
        string='Allow Payment Method Update', default=True)

    # Notifications
    notify_renewal_days = fields.Integer(string='Notify Before Renewal (days)',
                                         default=7)
    notify_payment_failed = fields.Boolean(string='Notify on Payment Failed',
                                           default=True)

    # Usage display
    show_usage = fields.Boolean(string='Show Usage Meters', default=True)
    usage_limit_alert = fields.Float(string='Usage Alert Threshold (%)',
                                     default=80.0)

    @api.depends('product_id', 'quantity')
    def _compute_recurring_monthly_amount(self):
        for sub in self:
            price = sub.product_id.list_price or 0.0
            sub.recurring_monthly_amount = price * (sub.quantity or 1.0)

    # ------------------------------------------------------------- lifecycle
    def _check_active(self):
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_(
                'Only active subscriptions support this action.'))

    def action_start(self):
        for sub in self.filtered(lambda s: s.state == 'draft'):
            if not sub.next_invoice_date:
                from dateutil.relativedelta import relativedelta
                sub.next_invoice_date = fields.Date.context_today(sub) \
                    + relativedelta(months=1)
            sub.state = 'active'
            sub.message_post(body=_('Subscription activated.'))

    def action_pause(self):
        for sub in self:
            sub._check_active()
            if not sub.allow_pause:
                raise UserError(_('Pausing is not allowed for this '
                                  'subscription.'))
            sub.state = 'paused'
            sub.message_post(body=_('Subscription paused via portal.'))

    def action_resume(self):
        for sub in self:
            if sub.state != 'paused':
                raise UserError(_('Only paused subscriptions can be '
                                  'resumed.'))
            sub.state = 'active'
            sub.message_post(body=_('Subscription resumed.'))

    def action_change_quantity(self, new_qty):
        """Upgrade/downgrade entry point used by the portal."""
        self.ensure_one()
        self._check_active()
        if new_qty <= 0:
            raise UserError(_('Quantity must be positive.'))
        direction = 'upgrade' if new_qty > self.quantity else 'downgrade'
        allowed = self.allow_upgrade if direction == 'upgrade' \
            else self.allow_downgrade
        if not allowed:
            raise UserError(_('%s is not allowed for this subscription.')
                            % direction.title())
        old = self.quantity
        self.quantity = new_qty
        self.message_post(body=_('%s: quantity %s -> %s.')
                          % (direction.title(), old, new_qty))

    def action_cancel(self):
        for sub in self:
            if not sub.allow_cancel:
                raise UserError(_('Cancellation is not allowed for this '
                                  'subscription.'))
            if sub.state == 'cancelled':
                continue
            sub.state = 'cancelled'
            sub.message_post(body=_('Subscription cancelled via portal.'))
