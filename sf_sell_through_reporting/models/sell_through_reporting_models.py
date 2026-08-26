# -*- coding: utf-8 -*-
"""Distributor Sell-Through Reporting models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSellThrough(models.Model):
    _name = 'sf.sell.through'
    _description = 'Sell-Through Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Distributor', required=True)
    period_month = fields.Date(string='Period', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    opening_stock = fields.Float(string='Opening Stock')
    purchases = fields.Float(string='Purchases from Us')
    sell_through_qty = fields.Float(string='Sold to End Market')
    closing_stock = fields.Float(string='Closing Stock')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('validated', 'Validated'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.sell.through') or 'NEW'
        return super().create(vals_list)

    def action_received(self):
        self.write({'state': 'received'})

    def action_validated(self):
        self.write({'state': 'validated'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.sell.through'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.sell.through'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
