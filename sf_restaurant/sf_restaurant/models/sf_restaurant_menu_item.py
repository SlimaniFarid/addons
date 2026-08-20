# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class SfRestaurantMenuItem(models.Model):
    _name = 'sf.restaurant.menu.item'
    _description = 'Restaurant Menu Item'
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    category_id = fields.Many2one('sf.restaurant.menu.category', string='Category', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', ondelete='set null')
    price_unit = fields.Monetary(string='Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    available_breakfast = fields.Boolean(string='Breakfast', default=True)
    available_lunch = fields.Boolean(string='Lunch', default=True)
    available_dinner = fields.Boolean(string='Dinner', default=True)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.restaurant.menu.item')
        return super().create(vals_list)

    def write(self, vals):
        if 'price_unit' in vals:
            self._check_manager()
        return super().write(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_restaurant.group_sf_restaurant_manager'):
            raise UserError(_('Only a restaurant manager can modify menu prices.'))