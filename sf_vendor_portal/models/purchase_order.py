# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_response = fields.Selection([
        ('draft', 'No Response'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('counter', 'Counter-offer'),
    ], string='Vendor Response', default='draft', copy=False,
        tracking=True, help="Response of the vendor to this document.")
    vendor_response_date = fields.Datetime(string='Response Date', copy=False)
    vendor_comment = fields.Text(string='Vendor Comment', copy=False)
    counter_total = fields.Monetary(string='Counter-offer Amount', copy=False,
                                    currency_field='currency_id')
    portal_access_key = fields.Char(string='Portal Access Key', copy=False,
                                    default=lambda self: self._default_access_key())

    def _default_access_key(self):
        import secrets
        return secrets.token_urlsafe(12)

    def _portal_action_guard(self):
        """Only RFQs actually sent to the vendor may be answered."""
        if self.state not in ('sent',):
            raise UserError(_(
                'This document is not awaiting a vendor response '
                '(current state: %s).') % self.state)

    def action_vendor_accept(self):
        """Called from the vendor portal when the vendor accepts the RFQ."""
        self.ensure_one()
        self._portal_action_guard()
        self.write({
            'vendor_response': 'accepted',
            'vendor_response_date': fields.Datetime.now(),
        })
        self.message_post(
            body=_('Vendor accepted this request for quotation.'))

    def action_vendor_decline(self, comment=False):
        """Called from the vendor portal when the vendor declines the RFQ."""
        self.ensure_one()
        self._portal_action_guard()
        self.write({
            'vendor_response': 'declined',
            'vendor_response_date': fields.Datetime.now(),
            'vendor_comment': comment or self.vendor_comment,
        })
        self.message_post(
            body=_('Vendor declined this request for quotation.'))

    def action_vendor_counter(self, amount):
        """Called from the vendor portal when the vendor proposes a price."""
        self.ensure_one()
        self._portal_action_guard()
        if not amount or amount <= 0:
            raise UserError(_('Counter-offer must be a positive amount.'))
        self.write({
            'vendor_response': 'counter',
            'vendor_response_date': fields.Datetime.now(),
            'counter_total': amount,
        })
        self.message_post(
            body=_('Vendor proposed a counter-offer of %s') % amount)