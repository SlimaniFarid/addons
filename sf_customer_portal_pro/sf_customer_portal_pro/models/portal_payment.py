from odoo import api, fields, models


class PortalPayment(models.Model):
    _name = 'portal.payment'
    _description = 'Portal Payment Record'
    _order = 'create_date desc'

    config_id = fields.Many2one('portal.config', string='Portal Config', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    invoice_id = fields.Many2one('account.move', string='Invoice', required=True, ondelete='cascade')

    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    currency_id = fields.Many2one(related='invoice_id.currency_id', store=True)

    provider_id = fields.Many2one('payment.provider', string='Payment Provider', required=True)
    transaction_id = fields.Many2one('payment.transaction', string='Odoo Transaction', ondelete='set null')

    state = fields.Selection([
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('error', 'Error'),
        ('refunded', 'Refunded'),
    ], string='Status', default='pending', tracking=True)

    external_reference = fields.Char(string='Provider Reference')
    error_message = fields.Text(string='Error')
    paid_date = fields.Datetime(string='Paid Date')

    def action_confirm(self):
        for pay in self.filtered(lambda p: p.state == 'pending'):
            # Trigger payment via provider
            if pay.transaction_id:
                pay.transaction_id._send_payment_request()
            pay.state = 'processing'

    def action_refund(self):
        for pay in self.filtered(lambda p: p.state == 'done'):
            if pay.transaction_id:
                pay.transaction_id._reconcile_after_done()
            pay.state = 'refunded'