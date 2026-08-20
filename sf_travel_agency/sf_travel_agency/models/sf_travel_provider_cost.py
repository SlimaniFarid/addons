# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfTravelProviderCost(models.Model):
    _name = 'sf.travel.provider.cost'
    _description = 'Provider Cost'
    _order = 'cost_date desc, id desc'

    name = fields.Char(string='Name', required=True, readonly=True, copy=False)
    reservation_id = fields.Many2one('sf.travel.reservation', string='Reservation', required=True, ondelete='cascade')
    provider_id = fields.Many2one('sf.travel.provider', string='Provider', required=True, ondelete='restrict')
    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    cost_date = fields.Date(string='Cost Date', default=fields.Date.context_today)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sf.travel.provider.cost') or 'New'
        return super(SfTravelProviderCost, self).create(vals)
