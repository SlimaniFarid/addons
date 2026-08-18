from odoo import api, fields, models


class PortalSubscriptionMgmt(models.Model):
    _name = 'portal.subscription.mgmt'
    _description = 'Portal Subscription Management'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    subscription_id = fields.Many2one('sale.subscription', string='Subscription', required=True, ondelete='cascade')

    # Portal-specific settings
    allow_upgrade = fields.Boolean(string='Allow Upgrade', default=True)
    allow_downgrade = fields.Boolean(string='Allow Downgrade', default=True)
    allow_cancel = fields.Boolean(string='Allow Cancel', default=True)
    allow_pause = fields.Boolean(string='Allow Pause', default=False)

    # Payment method management
    allow_payment_update = fields.Boolean(string='Allow Payment Method Update', default=True)
    default_payment_method_id = fields.Many2one('payment.token', string='Default Payment Method')

    # Notifications
    notify_renewal_days = fields.Integer(string='Notify Before Renewal (days)', default=7)
    notify_payment_failed = fields.Boolean(string='Notify on Payment Failed', default=True)

    # Usage display
    show_usage = fields.Boolean(string='Show Usage Meters', default=True)
    usage_limit_alert = fields.Float(string='Usage Alert Threshold (%)', default=80.0)

    def action_upgrade(self):
        # Redirect to upgrade wizard
        return {
            'type': 'ir.actions.act_window',
            'name': 'Upgrade Subscription',
            'res_model': 'portal.subscription.upgrade.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_subscription_id': self.subscription_id.id},
        }

    def action_cancel(self):
        # Cancel subscription with portal settings
        if self.allow_cancel:
            self.subscription_id.action_cancel()