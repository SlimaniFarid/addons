# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSalonService(models.Model):
    _name = 'sf.salon.service'
    _description = 'Salon Service'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    category = fields.Selection([
        ('haircut', 'Haircut'),
        ('color', 'Color'),
        ('styling', 'Styling'),
        ('manicure', 'Manicure'),
        ('skincare', 'Skincare'),
        ('makeup', 'Makeup'),
        ('other', 'Other'),
    ], string='Category', required=True, default='haircut')
    duration = fields.Integer(string='Duration (Minutes)', required=True)
    price = fields.Monetary(string='Price', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    commission_rate = fields.Float(string='Commission Rate (%)')
    product_id = fields.Many2one('product.product', string='Invoice Product', required=True, ondelete='restrict')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def _check_rate_edit(self, vals):
        if 'commission_rate' in vals and not self.env.user.has_group('sf_salon_beauty.group_sf_salon_manager'):
            raise UserError(_('Only a salon manager can set commission rates.'))

    def _get_default_duration(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('sf_salon_beauty.default_duration', '30'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.salon.service')
            self._check_rate_edit(vals)
            if 'duration' not in vals:
                vals['duration'] = self._get_default_duration()
        return super().create(vals_list)

    def write(self, vals):
        if 'commission_rate' in vals:
            self._check_rate_edit(vals)
        return super().write(vals)