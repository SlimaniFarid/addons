# -*- coding: utf-8 -*-
"""Expiry & FEFO Alert Manager models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfExpiryAlert(models.Model):
    _name = 'sf.expiry.alert'
    _description = 'Expiry Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    lot_id = fields.Many2one('stock.lot', string='Lot', required=True)
    product_id = fields.Many2one('product.product', string='Product')
    expiry_date = fields.Date(string='Expiry Date', required=True)
    alert_days = fields.Integer(string='Alert Before (days)', default=30)
    quantity = fields.Float(string='Quantity')
    disposition = fields.Selection([
        ('sell', 'Sell First (FEFO)'),
        ('discount', 'Discount'),
        ('write_off', 'Write Off'),
        ('donate', 'Donate'),
        ], string='Disposition', default=sell)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('actioned', 'Actioned'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.expiry.alert') or 'NEW'
        return super().create(vals_list)

    def action_actioned(self):
        self.write({'state': 'actioned'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.expiry.alert'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiry_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiry_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

