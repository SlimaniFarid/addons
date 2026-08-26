# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    portal_user_id = fields.Many2one('res.users', string='Portal User',
                                     help="Linked portal login for this vendor.")
    is_vendor_portal_user = fields.Boolean(
        string='Vendor Portal User',
        help="Check to give this vendor self-service portal access.")
    portal_welcome_sent = fields.Boolean(string='Welcome Sent', copy=False)
    total_quotation_count = fields.Integer(
        string='Total Quotations', compute='_compute_portal_counts',
        help="Number of RFQs sent to this vendor.")
    total_confirmed_orders = fields.Integer(
        string='Confirmed Orders', compute='_compute_portal_counts')

    @api.depends('is_vendor_portal_user')
    def _compute_portal_counts(self):
        for partner in self:
            purchase = self.env['purchase.order']
            partner.total_quotation_count = purchase.search_count([
                ('partner_id', '=', partner.id)])
            partner.total_confirmed_orders = purchase.search_count([
                ('partner_id', '=', partner.id),
                ('state', 'in', ['purchase', 'done'])])

    def action_create_portal_user(self):
        """Create a portal user for the vendor and send a welcome message."""
        self.ensure_one()
        if not self.portal_user_id:
            portal_group = self.env.ref('base.group_portal')
            user = self.env['res.users'].with_context(
                no_reset_password=False).create({
                    'partner_id': self.id,
                    'login': self.email,
                    'email': self.email,
                    'name': self.name,
                    'groups_id': [(6, 0, [portal_group.id])],
                })
            self.portal_user_id = user
        self.is_vendor_portal_user = True
        self.portal_welcome_sent = True
        self.message_post(
            body=_('Welcome %s! Your secure vendor portal is now available. '
                   'Sign in to see your quotations and orders.') % self.name)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }