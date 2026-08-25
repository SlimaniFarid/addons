# -*- coding: utf-8 -*-
from odoo import _, http
from odoo.http import request

VENDOR_MODEL = 'sf.vendor.onboarding.portal.vendor.onboarding'


class VendorOnboardingPortal(http.Controller):

    def _own_records(self):
        partner = request.env.user.partner_id
        return request.env[VENDOR_MODEL].sudo().search([
            ('partner_id', 'child_of', partner.id),
        ], order='create_date desc')

    def _is_owner(self, rec):
        user_partner = request.env.user.partner_id
        return rec.exists() and (
            rec.partner_id == user_partner
            or user_partner in rec.partner_id.child_ids)

    @http.route('/my/vendor-onboarding', type='http', auth='user',
                website=True)
    def portal_list(self, **kw):
        if not request.env.user.has_group('base.group_portal'):
            return request.redirect('/my')
        return request.render(
            'sf_vendor_onboarding_portal.portal_vendor_onboarding_list',
            {'records': self._own_records()})

    @http.route('/my/vendor-onboarding/new', type='http', auth='user',
                website=True, methods=['GET'])
    def portal_form(self, **kw):
        if not request.env.user.has_group('base.group_portal'):
            return request.redirect('/my')
        return request.render(
            'sf_vendor_onboarding_portal.portal_vendor_onboarding_form',
            {'error': False, 'values': {}})

    @http.route('/my/vendor-onboarding/submit', type='http', auth='user',
                website=True, methods=['POST'], csrf=True)
    def portal_submit(self, tax_id='', bank_account='', **post):
        if not request.env.user.has_group('base.group_portal'):
            return request.redirect('/my')
        Record = request.env[VENDOR_MODEL].sudo()
        rec = Record.create({
            'partner_id': request.env.user.partner_id.id,
            'tax_id': (tax_id or '').strip(),
            'bank_account': (bank_account or '').strip(),
        })
        if rec.state == 'draft':
            rec.write({'state': 'submitted'})
            rec.message_post(
                body=_('Vendor onboarding submitted via portal by %s.')
                % request.env.user.name)
        return request.redirect('/my/vendor-onboarding')

    @http.route('/my/vendor-onboarding/<int:rec_id>', type='http',
                auth='user', website=True)
    def portal_detail(self, rec_id, **kw):
        rec = request.env[VENDOR_MODEL].sudo().browse(rec_id)
        if not self._is_owner(rec):
            return request.redirect('/my/vendor-onboarding')
        return request.render(
            'sf_vendor_onboarding_portal.portal_vendor_onboarding_detail',
            {'record': rec})
