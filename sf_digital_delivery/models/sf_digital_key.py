# -*- coding: utf-8 -*-
import secrets
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_KEY_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'


class SfDigitalKey(models.Model):
    _name = 'sf.digital.key'
    _description = 'Digital License Key'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.digital.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    product_id = fields.Many2one('sf.digital.product', string='Digital Product', required=True,
                                 ondelete='restrict')
    key = fields.Char(string='Key', required=True, copy=False)
    order_id = fields.Many2one('sale.order', string='Sales Order', ondelete='set null')
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='set null')
    delivery_id = fields.Many2one('sf.digital.delivery', string='Digital Delivery',
                                  ondelete='set null')
    state = fields.Selection([
        ('generated', 'Generated'),
        ('delivered', 'Delivered'),
        ('activated', 'Activated'),
        ('revoked', 'Revoked'),
        ('expired', 'Expired'),
    ], string='Status', default='generated', copy=False)
    activation_count = fields.Integer(string='Activation Count', default=0, copy=False)
    activated_date = fields.Datetime(string='Activated On', copy=False)
    delivered_date = fields.Datetime(string='Delivered On', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('key_uniq', 'unique(key)', 'License keys must be unique.'),
        ('key_nonempty', "CHECK (key IS NOT NULL AND key != '')", 'The key cannot be empty.'),
        ('activation_non_negative', 'CHECK (activation_count >= 0)',
         'The activation count cannot be negative.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.digital.key')
            if not vals.get('company_id'):
                if vals.get('delivery_id'):
                    delivery = self.env['sf.digital.delivery'].browse(vals['delivery_id'])
                    vals['company_id'] = delivery.company_id.id
                elif vals.get('product_id'):
                    product = self.env['sf.digital.product'].browse(vals['product_id'])
                    vals['company_id'] = product.company_id.id
        return super().create(vals_list)

    @api.model
    def _make_unique_key(self, key_format, company_id):
        segments = key_format.split('-') if key_format else ['XXXX', 'XXXX', 'XXXX']
        for _attempt in range(100):
            parts = []
            for segment in segments:
                length = len(segment) if segment else 4
                parts.append(''.join(secrets.choice(_KEY_ALPHABET) for _ in range(length)))
            candidate = '-'.join(parts)
            if not self.with_company(company_id).search_count([('key', '=', candidate)]):
                return candidate
        raise UserError(_('Unable to generate a unique license key.'))

    @api.model
    def _generate_keys(self, line):
        key_format = line.digital_product_id.key_format
        if not key_format:
            key_format = self.env['ir.config_parameter'].sudo().get_param(
                'sf_digital_delivery.default_key_format', 'XXXX-XXXX-XXXX')
        existing = len(line.key_ids)
        needed = line.quantity - existing
        for _i in range(needed):
            candidate = self._make_unique_key(key_format, line.company_id.id)
            self.create({
                'product_id': line.digital_product_id.id,
                'key': candidate,
                'order_id': line.delivery_id.order_id.id,
                'partner_id': line.delivery_id.partner_id.id,
                'delivery_id': line.delivery_id.id,
                'company_id': line.company_id.id,
            })

    def action_activate(self):
        for key in self:
            if key.state != 'delivered':
                raise UserError(_('Only delivered keys can be activated.'))
            if key.activation_count >= key.product_id.max_activations:
                raise UserError(_('The activation limit (%s) has been reached for this key.') %
                                key.product_id.max_activations)
            key.write({
                'activation_count': key.activation_count + 1,
                'activated_date': fields.Datetime.now(),
                'state': 'activated',
            })
            key.message_post(body=_('The key was activated.'))

    def action_revoke(self):
        if not self.env.user.has_group('sf_digital_delivery.group_sf_digital_delivery_manager'):
            raise UserError(_('Only a digital delivery manager can revoke keys.'))
        for key in self:
            if key.state not in ('delivered', 'activated'):
                raise UserError(_('Only delivered or activated keys can be revoked.'))
            key.state = 'revoked'
            key.message_post(body=_('The key was revoked.'))