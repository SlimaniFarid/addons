# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class VendorPortalSettings(models.Model):
    _name = 'sf.vendor.portal.settings'
    _description = 'Vendor Portal Settings'
    _rec_name = 'name'

    name = fields.Char(string='Name', default='Vendor Portal')
    welcome_message = fields.Text(
        string='Welcome Message',
        default='Welcome to our vendor portal. Track your quotations, '
                'orders and invoices online.')
    auto_create_portal_user = fields.Boolean(
        string='Auto-create Portal Users',
        help="Automatically create a portal login when a vendor is created.")
    notify_on_rfq = fields.Boolean(
        string='Notify Vendors on New RFQ',
        help="Send an email to vendors when a new RFQ is sent.")
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)

    @api.model
    def _get_settings(self):
        return self.search([], limit=1) or self.create({})