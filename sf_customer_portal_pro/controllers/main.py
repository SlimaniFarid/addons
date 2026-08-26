# -*- coding: utf-8 -*-
from odoo import _, fields, http
from odoo.http import request


class CustomerPortalPro(http.Controller):

    # ------------------------------------------------------------ helpers
    def _portal_user(self):
        return request.env.user.has_group('base.group_portal') or \
            request.env.user.has_group('base.group_user')

    def _partner(self):
        return request.env.user.partner_id

    def _config(self):
        Config = request.env['portal.config']
        cfg = Config.search([], limit=1)
        return cfg or Config.create({'name': 'Portal Config'})

    def _own(self, model, extra_domain=None):
        domain = [('partner_id', 'child_of', self._partner().id)]
        if extra_domain:
            domain += extra_domain
        return request.env[model].sudo().search(domain)

    def _is_owner(self, rec):
        partner = self._partner()
        return rec.exists() and (
            rec.partner_id == partner or partner in rec.partner_id.child_ids)

    # ---------------------------------------------------------- dashboard
    @http.route('/my/dashboard', type='http', auth='user', website=True)
    def dashboard(self, **kw):
        if not self._portal_user():
            return request.redirect('/my')
        invoices = request.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice'),
            ('partner_id', 'child_of', self._partner().id),
            ('payment_state', 'in', ('not_paid', 'partial')),
        ], limit=10)
        tickets = self._own('portal.ticket', [('state', '!=', 'closed')])
        subs = self._own('portal.subscription.mgmt',
                         [('state', '=', 'active')])
        docs = self._own('portal.document')
        return request.render(
            'sf_customer_portal_pro.portal_dashboard',
            {'open_invoices': invoices,
             'open_total': sum(invoices.mapped('amount_residual')),
             'open_tickets': tickets,
             'active_subscriptions': subs,
             'documents_count': len(docs)})

    # ----------------------------------------------------------- invoices
    @http.route('/my/invoices', type='http', auth='user', website=True)
    def invoices(self, **kw):
        records = request.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice'),
            ('partner_id', 'child_of', self._partner().id),
        ], order='invoice_date_due asc')
        return request.render(
            'sf_customer_portal_pro.portal_invoices',
            {'records': records})

    @http.route('/my/invoices/<int:inv_id>/pay', type='http',
                auth='user', website=True)
    def invoice_pay(self, inv_id, **kw):
        """Redirect to the standard payment flow of the `payment` module."""
        move = request.env['account.move'].sudo().browse(inv_id)
        if not move.exists() or not self._is_owner(move) \
           or move.payment_state not in ('not_paid', 'partial'):
            return request.redirect('/my/invoices')
        return request.redirect(
            '/payment/pay?move_ids=%d&amount=%s'
            % (move.id, move.amount_residual))

    # ------------------------------------------------------------- tickets
    @http.route('/my/tickets', type='http', auth='user', website=True)
    def tickets(self, **kw):
        return request.render(
            'sf_customer_portal_pro.portal_tickets',
            {'records': self._own('portal.ticket')})

    @http.route('/my/tickets/new', type='http', auth='user',
                methods=['GET'], website=True)
    def ticket_form(self, **kw):
        return request.render(
            'sf_customer_portal_pro.portal_ticket_form',
            {'error': kw.get('error'), 'categories':
                request.env['portal.ticket']._fields['category'].selection})

    @http.route('/my/tickets/submit', type='http', auth='user',
                methods=['POST'], csrf=True, website=True)
    def ticket_submit(self, subject='', category='general', priority='1',
                      description='', **post):
        if not (subject or '').strip():
            return request.redirect('/my/tickets/new?error=subject')
        request.env['portal.ticket'].sudo().create({
            'config_id': self._config().id,
            'name': subject.strip(),
            'category': category,
            'priority': priority,
            'description': description or '',
            'partner_id': self._partner().id,
        })
        return request.redirect('/my/tickets')

    @http.route('/my/tickets/<int:rec_id>', type='http', auth='user',
                website=True)
    def ticket_detail(self, rec_id, **kw):
        rec = request.env['portal.ticket'].sudo().browse(rec_id)
        if not self._is_owner(rec):
            return request.redirect('/my/tickets')
        messages = rec.message_ids.filtered(lambda m: m.body)[:20]
        return request.render(
            'sf_customer_portal_pro.portal_ticket_detail',
            {'record': rec, 'messages': messages})

    @http.route('/my/tickets/<int:rec_id>/comment', type='http',
                auth='user', methods=['POST'], csrf=True)
    def ticket_comment(self, rec_id, message='', **post):
        rec = request.env['portal.ticket'].sudo().browse(rec_id)
        if self._is_owner(rec) and (message or '').strip():
            rec.message_post(body=message.strip(),
                             author_id=request.env.user.partner_id.id,
                             message_type='comment',
                             subtype_xmlid='mail.mt_comment')
        return request.redirect(f'/my/tickets/{rec_id}')

    # ----------------------------------------------------------- documents
    @http.route('/my/documents', type='http', auth='user', website=True)
    def documents(self, **kw):
        return request.render(
            'sf_customer_portal_pro.portal_documents',
            {'records': self._own('portal.document')})

    # -------------------------------------------------------- subscriptions
    @http.route('/my/subscriptions', type='http', auth='user', website=True)
    def subscriptions(self, **kw):
        return request.render(
            'sf_customer_portal_pro.portal_subscriptions',
            {'records': self._own('portal.subscription.mgmt')})

    @http.route('/my/subscriptions/<int:rec_id>/qty', type='http',
                auth='user', methods=['POST'], csrf=True)
    def subscription_qty(self, rec_id, quantity='', **post):
        sub = request.env['portal.subscription.mgmt'].sudo().browse(rec_id)
        try:
            qty = float(quantity)
        except (TypeError, ValueError):
            qty = 0
        if self._is_owner(sub):
            try:
                sub.action_change_quantity(qty)
            except Exception as exc:
                return request.render(
                    'sf_customer_portal_pro.portal_error',
                    {'message': str(exc)})
        return request.redirect('/my/subscriptions')

    @http.route(['/my/subscriptions/<int:rec_id>/pause',
                 '/my/subscriptions/<int:rec_id>/resume',
                 '/my/subscriptions/<int:rec_id>/cancel'],
                type='http', auth='user', methods=['POST'], csrf=True)
    def subscription_lifecycle(self, **post):
        path = request.httprequest.path.rstrip('/').split('/')
        rec_id, action = int(path[-2]), path[-1]
        sub = request.env['portal.subscription.mgmt'].sudo().browse(rec_id)
        method = getattr(sub, f'action_{action}', None) \
            if self._is_owner(sub) else None
        if method:
            try:
                method()
            except Exception as exc:
                return request.render(
                    'sf_customer_portal_pro.portal_error',
                    {'message': str(exc)})
        return request.redirect('/my/subscriptions')
