# -*- coding: utf-8 -*-
"""Multi-Site Price Harmony Check models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPriceHarmony(models.Model):
    _name = 'sf.price.harmony'
    _description = 'Price Harmony Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    site_a = fields.Char(string='Site A', required=True)
    site_b = fields.Char(string='Site B', required=True)
    price_a = fields.Float(string='Price A')
    price_b = fields.Float(string='Price B')
    gap_percent = fields.Float(string='Gap %')
    harmonized_to = fields.Float(string='Harmonized To')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('detected', 'Detected'),
        ('harmonized', 'Harmonized'),
        ('justified', 'Justified - Kept'),
        ], string='Status', default='detected', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.price.harmony') or 'NEW'
        return super().create(vals_list)

    def action_harmonized(self):
        self.write({'state': 'harmonized'})

    def action_justified(self):
        self.write({'state': 'justified'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.price.harmony'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.price.harmony'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
