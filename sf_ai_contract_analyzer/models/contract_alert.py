from odoo import api, fields, models


class ContractAlert(models.Model):
    _name = 'contract.alert'
    _description = 'Contract Alert'
    _order = 'trigger_date, id'

    document_id = fields.Many2one('contract.document', string='Contract', required=True, ondelete='cascade')

    alert_type = fields.Selection([
        ('renewal', 'Renewal Due'),
        ('notice_period', 'Notice Period Starting'),
        ('expiration', 'Contract Expiring'),
        ('obligation_due', 'Obligation Due'),
        ('payment_due', 'Payment Due'),
        ('review', 'Review Required'),
        ('price_review', 'Price Review'),
        ('compliance', 'Compliance Deadline'),
        ('custom', 'Custom Alert'),
    ], string='Alert Type', required=True)

    title = fields.Char(string='Alert Title', required=True)
    description = fields.Html(string='Description')

    # Timing
    trigger_date = fields.Date(string='Trigger Date', required=True)
    advance_days = fields.Integer(string='Advance Notice (Days)', default=30)
    send_at = fields.Date(string='Send Date', compute='_compute_send_at', store=True)

    # Recipients
    recipient_ids = fields.Many2many('res.users', string='Recipients')
    send_email = fields.Boolean(string='Send Email', default=True)
    send_notification = fields.Boolean(string='Send In-App Notification', default=True)

    # Status
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('dismissed', 'Dismissed'),
    ], string='State', default='scheduled')

    # Email template
    email_template_id = fields.Many2one('mail.template', string='Email Template')

    @api.depends('trigger_date', 'advance_days')
    def _compute_send_at(self):
        for alert in self:
            if alert.trigger_date and alert.advance_days:
                from datetime import timedelta
                alert.send_at = alert.trigger_date - timedelta(days=alert.advance_days)
            else:
                alert.send_at = alert.trigger_date

    def action_send(self):
        for alert in self.filtered(lambda a: a.state == 'scheduled'):
            # Send email/notification
            alert.state = 'sent'

    @api.autovacuum
    def _check_due_alerts(self):
        today = fields.Date.today()
        due_alerts = self.search([
            ('state', '=', 'scheduled'),
            ('send_at', '<=', today),
        ])
        for alert in due_alerts:
            alert.action_send()