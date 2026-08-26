# -*- coding: utf-8 -*-
from odoo import fields, models


class SfRestaurantZone(models.Model):
    _name = 'sf.restaurant.zone'
    _description = 'Restaurant Zone'
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    table_ids = fields.One2many('sf.restaurant.table', 'zone_id', string='Tables')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.restaurant.zone')
        return super().create(vals_list)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.restaurant.activity.mixin'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

