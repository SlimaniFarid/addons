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

    def action_mark_paid(self):
        """Confirm reconciliation once the provider webhook confirmed."""
        for pay in self.filtered(lambda p: p.state == 'processing'):
            pay.write({'state': 'done',
                       'paid_date': fields.Datetime.now()})

    def action_refund(self):
        """Real money-back path: reverse the invoice (credit note) then flag
        the portal payment as refunded. The provider-side capture reversal is
        driven by the standard payment module when a transaction exists."""
        for pay in self.filtered(lambda p: p.state == 'done'):
            if not pay.invoice_id:
                continue
            reversal = self.env['account.move.reversal'].with_context(
                active_model='account.move',
                active_ids=pay.invoice_id.ids,
            ).create({
                'move_ids': [(6, 0, pay.invoice_id.ids)],
                'reason': 'Portal refund %s' % pay.display_name,
            })
            res = reversal.action_reverse()
            pay.transaction_id and pay.transaction_id._log_message_on(
                pay.invoice_id, 'Refund requested from customer portal.')
            pay.state = 'refunded'