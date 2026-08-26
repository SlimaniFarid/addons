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

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.vendor.portal.settings'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.vendor.portal.settings'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
