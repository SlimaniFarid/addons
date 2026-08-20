# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfShareholder(models.Model):
    _name = 'sf.shareholder'
    _description = 'Shareholder'
    _order = 'name asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner')
    function = fields.Char(string='Function')
    total_shares = fields.Integer(
        string='Total Shares', compute='_compute_totals', store=True)
    total_value = fields.Monetary(
        string='Capital Value', compute='_compute_totals', store=True,
        currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        related='company_id.currency_id', readonly=True, store=True)
    capital_movement_ids = fields.One2many(
        'sf.capital.movement', 'shareholder_id', string='Capital Movements')
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    @api.depends('capital_movement_ids.state',
                 'capital_movement_ids.quantity',
                 'capital_movement_ids.direction',
                 'capital_movement_ids.amount')
    def _compute_totals(self):
        for holder in self:
            moves = holder.capital_movement_ids.filtered(
                lambda m: m.state == 'posted')
            shares = 0
            value = 0.0
            for move in moves:
                sign = 1 if move.direction == 'buy' else -1
                shares += sign * move.quantity
                value += sign * move.amount
            holder.total_shares = shares
            holder.total_value = value

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.shareholder')
        return super().create(vals_list)