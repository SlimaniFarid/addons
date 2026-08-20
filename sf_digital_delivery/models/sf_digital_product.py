# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SfDigitalProduct(models.Model):
    _name = 'sf.digital.product'
    _description = 'Digital Product'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.digital.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    product_id = fields.Many2one('product.template', string='Saleable Product', required=True)
    delivery_type = fields.Selection([
        ('license_key', 'License Key'),
        ('download', 'Download Link'),
    ], string='Delivery Type', required=True, default='license_key')
    key_format = fields.Char(string='Key Format', help='License key format, e.g. XXXX-XXXX-XXXX')
    max_activations = fields.Integer(string='Max Activations', default=1)
    validity_days = fields.Integer(string='Link Validity (days)', default=30)
    file_binary = fields.Binary(string='File to Download')
    file_name = fields.Char(string='File Name')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.digital.product')
            if not vals.get('key_format'):
                vals['key_format'] = self.env['ir.config_parameter'].sudo().get_param(
                    'sf_digital_delivery.default_key_format', 'XXXX-XXXX-XXXX')
            if not vals.get('validity_days'):
                default_validity = self.env['ir.config_parameter'].sudo().get_param(
                    'sf_digital_delivery.default_validity_days', '30')
                vals['validity_days'] = int(default_validity)
        return super().create(vals_list)

    def write(self, vals):
        if 'delivery_type' in vals and 'key_format' not in vals:
            for record in self:
                if record.delivery_type == 'license_key' and not record.key_format:
                    vals['key_format'] = self.env['ir.config_parameter'].sudo().get_param(
                        'sf_digital_delivery.default_key_format', 'XXXX-XXXX-XXXX')
                    break
        return super().write(vals)