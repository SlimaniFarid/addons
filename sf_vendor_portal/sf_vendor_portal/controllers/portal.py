# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class VendorPortal(http.Controller):

    @http.route('/my/vendor', type='http', auth='user', website=True)
    def vendor_home(self):
        partner = request.env.user.partner_id
        if not partner.is_vendor_portal_user:
            return request.redirect('/my')
        purchase = request.env['purchase.order'].sudo().search(
            [('partner_id', '=', partner.id)], order='date_order desc')
        return request.render(
            'sf_vendor_portal.vendor_portal_home',
            {'purchase_orders': purchase})

    @http.route('/my/vendor/rfq/<int:order_id>', type='http', auth='user',
                website=True)
    def vendor_rfq_detail(self, order_id):
        partner = request.env.user.partner_id
        order = request.env['purchase.order'].sudo().browse(order_id)
        if order.partner_id.id != partner.id:
            return request.redirect('/my/vendor')
        return request.render(
            'sf_vendor_portal.vendor_rfq_detail', {'order': order})

    @http.route('/my/vendor/rfq/<int:order_id>/accept', type='json',
                auth='user', website=True)
    def vendor_accept(self, order_id):
        partner = request.env.user.partner_id
        order = request.env['purchase.order'].sudo().browse(order_id)
        if order.partner_id.id != partner.id:
            return {'error': 'forbidden'}
        order.action_vendor_accept()
        return {'success': True}

    @http.route('/my/vendor/rfq/<int:order_id>/decline', type='json',
                auth='user', website=True)
    def vendor_decline(self, order_id, comment=''):
        partner = request.env.user.partner_id
        order = request.env['purchase.order'].sudo().browse(order_id)
        if order.partner_id.id != partner.id:
            return {'error': 'forbidden'}
        order.action_vendor_decline(comment)
        return {'success': True}

    @http.route('/my/vendor/rfq/<int:order_id>/counter', type='json',
                auth='user', website=True)
    def vendor_counter(self, order_id, amount=0.0):
        partner = request.env.user.partner_id
        order = request.env['purchase.order'].sudo().browse(order_id)
        if order.partner_id.id != partner.id:
            return {'error': 'forbidden'}
        order.action_vendor_counter(float(amount))
        return {'success': True}