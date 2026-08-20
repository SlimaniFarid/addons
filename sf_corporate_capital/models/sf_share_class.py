# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfShareClass(models.Model):
    _name = 'sf.share.class'
    _description = 'Share Class'
    _order = 'name asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    nominal_value = fields.Monetary(
        string='Nominal Value', currency_field='currency_id')
    authorized_shares = fields.Integer(string='Authorized Shares')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        related='company_id.currency_id', readonly=True, store=True)
    issued_shares = fields.Integer(
        string='Issued Shares', compute='_compute_issued_shares', store=True)
    capital_movement_ids = fields.One2many(
        'sf.capital.movement', 'share_class_id', string='Capital Movements')
    company_id = fields.Many2one(
        'res.company', string='Company', store=True,
        default=lambda self: self.env.company)

    @api.depends('capital_movement_ids.state',
                 'capital_movement_ids.quantity',
                 'capital_movement_ids.direction')
    def _compute_issued_shares(self):
        for share_class in self:
            moves = share_class.capital_movement_ids.filtered(
                lambda m: m.state == 'posted')
            issued = 0
            for move in moves:
                issued += move.quantity if move.direction == 'buy' \
                    else -move.quantity
            share_class.issued_shares = issued

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.share.class')
        return super().create(vals_list)