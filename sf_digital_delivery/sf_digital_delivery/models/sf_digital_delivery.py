# -*- coding: utf-8 -*-
import secrets
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfDigitalDelivery(models.Model):
    _name = 'sf.digital.delivery'
    _description = 'Digital Delivery'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.digital.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    order_id = fields.Many2one('sale.order', string='Sales Order', required=True,
                               ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 related='order_id.partner_id', store=True, readonly=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    line_ids = fields.One2many('sf.digital.delivery.line', 'delivery_id', string='Lines')
    delivery_date = fields.Datetime(string='Delivery Date', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.digital.delivery')
        return super().create(vals_list)

    @api.model
    def _create_from_order(self, order):
        existing = self.search([('order_id', '=', order.id)])
        if existing:
            return existing[0]
        lines_map = {}
        for line in order.order_line:
            tmpl = line.product_id.product_tmpl_id
            digital = self.env['sf.digital.product'].search([
                ('product_id', '=', tmpl.id),
                ('company_id', '=', order.company_id.id),
            ], limit=1)
            if digital:
                qty = int(line.product_uom_qty)
                if qty > 0:
                    lines_map.setdefault(digital.id, 0)
                    lines_map[digital.id] += qty
        if not lines_map:
            return False
        delivery = self.with_company(order.company_id).create({
            'order_id': order.id,
            'company_id': order.company_id.id,
        })
        for digital_id, qty in lines_map.items():
            digital_product = self.env['sf.digital.product'].browse(digital_id)
            self.env['sf.digital.delivery.line'].with_company(order.company_id).create({
                'delivery_id': delivery.id,
                'product_id': digital_product.product_id.id,
                'digital_product_id': digital_product.id,
                'quantity': qty,
            })
        delivery.message_post(
            body=_('A digital delivery was created automatically on order confirmation.'))
        return delivery

    def _check_manager(self):
        if not self.env.user.has_group('sf_digital_delivery.group_sf_digital_delivery_manager'):
            raise UserError(_('Only a digital delivery manager can perform this action.'))

    def _generate_download_url(self, line):
        token = secrets.token_urlsafe(24)
        return 'https://example.com/download/%s' % token

    def action_generate_keys(self):
        self._check_manager()
        for delivery in self:
            if delivery.state != 'draft':
                raise UserError(_('Only draft deliveries can be generated.'))
            for line in delivery.line_ids:
                if line.digital_product_id.delivery_type == 'license_key':
                    self.env['sf.digital.key']._generate_keys(line)
                else:
                    line.download_url = self._generate_download_url(line)
            delivery.state = 'generated'
            delivery.message_post(body=_('License keys and/or download links were generated.'))

    def action_deliver(self):
        self._check_manager()
        for delivery in self:
            if delivery.state != 'generated':
                raise UserError(_('Only generated deliveries can be delivered.'))
            missing = delivery.line_ids.filtered(
                lambda line: line.digital_product_id.delivery_type == 'license_key'
                and not line.key_ids)
            if missing:
                delivery.state = 'failed'
                raise UserError(
                    _('The delivery cannot be delivered because some license lines have no '
                      'generated keys.'))
            body_lines = []
            for line in delivery.line_ids:
                if line.digital_product_id.delivery_type == 'license_key':
                    line.key_ids.write({
                        'state': 'delivered',
                        'delivered_date': fields.Datetime.now(),
                    })
                    keys_text = ', '.join(line.key_ids.mapped('key')) or _('no key')
                    body_lines.append(_('%s: keys %s') % (line.product_id.name, keys_text))
                else:
                    body_lines.append(_('%s: download link %s') %
                                      (line.product_id.name, line.download_url))
            delivery.write({
                'delivery_date': fields.Datetime.now(),
                'state': 'delivered',
            })
            delivery.message_post(
                body=_('Digital goods delivered to the customer: %s') % '; '.join(body_lines))

    def action_fail(self):
        self._check_manager()
        for delivery in self:
            if delivery.state not in ('draft', 'generated'):
                raise UserError(_('Only draft or generated deliveries can be marked as failed.'))
            delivery.state = 'failed'
            delivery.message_post(body=_('The delivery was marked as failed.'))

    def action_cancel(self):
        for delivery in self:
            if delivery.state == 'delivered':
                raise UserError(_('Delivered deliveries cannot be cancelled.'))
            delivery.state = 'cancelled'
            delivery.message_post(body=_('The delivery was cancelled.'))

    def write(self, vals):
        protected = {'order_id', 'state', 'line_ids', 'delivery_date', 'partner_id'}
        for delivery in self:
            if delivery.state in ('delivered', 'cancelled') and any(
                    field in vals for field in protected):
                raise UserError(_('Delivered or cancelled deliveries are immutable.'))
        return super().write(vals)

    def _cron_daily_checks(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        activation_param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_digital_delivery.default_activation_days', '30')
        activation_days = int(activation_param)
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            cutoff = today - timedelta(days=activation_days)
            cutoff_dt = fields.Datetime.to_string(
                datetime.combine(cutoff, datetime.min.time()))
            expired_keys = scoped.env['sf.digital.key'].search([
                ('state', '=', 'delivered'),
                ('activation_count', '=', 0),
                ('delivered_date', '<', cutoff_dt),
            ])
            for key in expired_keys:
                key.state = 'expired'
                key.message_post(body=_('The key expired because it was never activated.'))
            deliveries = scoped.env['sf.digital.delivery'].search([
                ('state', '=', 'delivered'),
            ])
            for delivery in deliveries:
                expired_lines = delivery.line_ids.filtered(
                    lambda line: line.download_url and line.download_expired)
                if expired_lines:
                    delivery._sf_check_todo(
                        todo_type,
                        _('Download links have expired for delivery %s') % delivery.name,
                        _('Regenerate a link or cancel the delivery if required.'),
                    )


class SfDigitalDeliveryLine(models.Model):
    _name = 'sf.digital.delivery.line'
    _description = 'Digital Delivery Line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.digital.activity.mixin']
    _order = 'id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    delivery_id = fields.Many2one('sf.digital.delivery', string='Delivery', required=True,
                                  ondelete='cascade')
    product_id = fields.Many2one('product.template', string='Product', required=True,
                                 ondelete='restrict')
    digital_product_id = fields.Many2one('sf.digital.product', string='Digital Product',
                                         required=True, ondelete='restrict')
    quantity = fields.Integer(string='Quantity', required=True, default=1)
    key_ids = fields.One2many('sf.digital.key', 'delivery_id', string='License Keys')
    download_url = fields.Char(string='Download Link', copy=False)
    download_expiry_date = fields.Date(string='Download Expiry', compute='_compute_download_expiry',
                                       store=True)
    download_expired = fields.Boolean(string='Download Expired',
                                      compute='_compute_download_expiry', store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.digital.delivery.line')
            if not vals.get('company_id') and vals.get('delivery_id'):
                delivery = self.env['sf.digital.delivery'].browse(vals['delivery_id'])
                vals['company_id'] = delivery.company_id.id
        return super().create(vals_list)

    @api.depends('delivery_id.delivery_date', 'digital_product_id.validity_days', 'download_url')
    def _compute_download_expiry(self):
        today = fields.Date.context_today(self)
        for line in self:
            if (line.download_url and line.digital_product_id and line.digital_product_id.validity_days
                    and line.delivery_id.delivery_date):
                expiry = (line.delivery_id.delivery_date +
                          timedelta(days=line.digital_product_id.validity_days)).date()
                line.download_expiry_date = expiry
                line.download_expired = expiry < today
            else:
                line.download_expiry_date = False
                line.download_expired = False