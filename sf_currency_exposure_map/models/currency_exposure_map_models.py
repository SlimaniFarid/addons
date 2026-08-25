# -*- coding: utf-8 -*-
"""Currency Exposure Heatmap models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCurrency_exposure_map(models.Model):
    _name = 'sf.currency_exposure_map'
    _description = 'Currency Exposure Heatmap'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    currency_pair = fields.Char(string='Currency Pair', required=True)
    net_exposure = fields.Monetary(string='Net Exposure')
    hedged_percent = fields.Float(string='Hedged %')
    recommendation = fields.Text(string='Hedging Recommendation')
    currency_id = fields.Many2one(related='company_id.currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.currency_exposure_map') or 'NEW'
        return super().create(vals_list)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.currency_exposure_map'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
