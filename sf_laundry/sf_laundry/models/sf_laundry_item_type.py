# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class SfLaundryItemType(models.Model):
    _name = 'sf.laundry.item.type'
    _description = 'Laundry Item Type'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    service = fields.Selection([
        ('wash', 'Wash'),
        ('dry_clean', 'Dry Clean'),
        ('iron', 'Iron'),
        ('full_service', 'Full Service'),
    ], string='Service', required=True, default='wash')
    price_unit = fields.Monetary(string='Price', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.laundry.item.type')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_laundry.group_sf_laundry_manager'):
            raise UserError(_('Only a laundry manager can perform this action.'))

    def write(self, vals):
        if 'price_unit' in vals:
            self._check_manager()
        return super().write(vals)