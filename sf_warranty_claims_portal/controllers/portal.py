# -*- coding: utf-8 -*-
from odoo import _, fields, http
from odoo.http import request

CLAIM_MODEL = 'sf.warranty.claims.portal.warranty.claim'


class WarrantyClaimsPortal(http.Controller):

    def _own_records(self):
        return request.env[CLAIM_MODEL].sudo().search([
            ('partner_id', 'child_of', request.env.user.partner_id.id),
        ], order='create_date desc')

    def _is_owner(self, rec):
        user_partner = request.env.user.partner_id
        return rec.exists() and (
            rec.partner_id == user_partner
            or user_partner in rec.partner_id.child_ids)

    def _available_products(self):
        partner = request.env.user.partner_id
        # products invoiced to this partner first, fallback to saleable
        inv = request.env['account.move.line'].sudo().search_read(
            [('move_id.move_type', '=', 'out_invoice'),
             ('move_id.partner_id', 'child_of', partner.id),
             ('product_id', '!=', False)],
            ['product_id'])
        ids = list({l['product_id'][0] for l in inv})
        Product = request.env['product.product'].sudo()
        if ids:
            return Product.browse(ids)
        return Product.search([('sale_ok', '=', True)], limit=200)

    @http.route('/my/warranty-claims', type='http', auth='user',
                website=True)
    def portal_list(self, **kw):
        if not request.env.user.has_group('base.group_portal'):
            return request.redirect('/my')
        return request.render(
            'sf_warranty_claims_portal.portal_warranty_claims_list',
            {'records': self._own_records()})

    @http.route('/my/warranty-claims/new', type='http', auth='user',
                website=True, methods=['GET'])
    def portal_form(self, **kw):
        if not request.env.user.has_group('base.group_portal'):
            return request.redirect('/my')
        return request.render(
            'sf_warranty_claims_portal.portal_warranty_claims_form',
            {'products': self._available_products(),
             'error': kw.get('error')})

    @http.route('/my/warranty-claims/submit', type='http', auth='user',
                website=True, methods=['POST'], csrf=True)
    def portal_submit(self, product_id='', lot_serial='', description='',
                      **post):
        if not request.env.user.has_group('base.group_portal'):
            return request.redirect('/my')
        try:
            product = int(product_id)
        except (TypeError, ValueError):
            return request.redirect('/my/warranty-claims/new'
                                    '?error=missing_product')
        Claim = request.env[CLAIM_MODEL].sudo()
        product_rec = request.env['product.product'].sudo().browse(product)
        lot = False
        if lot_serial:
            lot = request.env['stock.lot'].sudo().search([
                ('product_id', '=', product),
                ('name', '=', lot_serial.strip()),
            ], limit=1)
        claim = Claim.create({
            'partner_id': request.env.user.partner_id.id,
            'product_id': product_rec.id,
            'lot_id': lot.id if lot else False,
            'description': description or '',
            'claim_date': fields.Date.today(),
        })
        claim.write({'state': 'submitted'})
        if not claim.sla_deadline:
            # SLA promise: acknowledge within 14 days (business default)
            from dateutil.relativedelta import relativedelta
            claim.sla_deadline = fields.Date.context_today(claim) \
                + relativedelta(days=14)
        claim.message_post(body=_(
            'Warranty claim submitted via portal by %s.')
            % request.env.user.name)
        return request.redirect('/my/warranty-claims')

    @http.route('/my/warranty-claims/<int:rec_id>', type='http',
                auth='user', website=True)
    def portal_detail(self, rec_id, **kw):
        rec = request.env[CLAIM_MODEL].sudo().browse(rec_id)
        if not self._is_owner(rec):
            return request.redirect('/my/warranty-claims')
        return request.render(
            'sf_warranty_claims_portal.portal_warranty_claims_detail',
            {'record': rec})

    @http.route('/my/warranty-claims/<int:rec_id>/cancel', type='http',
                auth='user', methods=['POST'], csrf=True)
    def portal_cancel(self, rec_id, **post):
        rec = request.env[CLAIM_MODEL].sudo().browse(rec_id)
        if not self._is_owner(rec) \
           or rec.state not in ('draft', 'submitted'):
            return request.redirect('/my/warranty-claims')
        rec.action_cancel()
        return request.redirect('/my/warranty-claims')
