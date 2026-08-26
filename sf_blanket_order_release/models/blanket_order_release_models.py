# -*- coding: utf-8 -*-
"""Blanket Order Release Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBlanketOrder(models.Model):
    _name = 'sf.blanket.order'
    _description = 'Blanket Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    total_quantity = fields.Float(string='Total Quantity')
    released_quantity = fields.Float(string='Released')
    unit_price = fields.Float(string='Unit Price')
    expiry_date = fields.Date(string='Expiry Date')
    remaining = fields.Float(string='Remaining')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('exhausted', 'Exhausted'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.blanket.order') or 'NEW'
        return super().create(vals_list)

    def action_exhausted(self):
        self.write({'state': 'exhausted'})

    def action_expired(self):
        self.write({'state': 'expired'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.blanket.order'

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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.blanket.order'

    def action_refresh_business(self):
        """Pull PO count and total for linked vendor."""
        for rec in self:
            vendor = getattr(rec, 'vendor_id',
                             getattr(rec, 'partner_id', False))
            if not vendor:
                continue
            pos = self.env['purchase.order'].search([
                ('partner_id', '=', vendor.id),
                ('state', 'in', ('purchase', 'done'))])
            rec.message_post(body=_(
                '{n} confirmed PO(s), total {t:.2f}.').format(
                n=len(pos), t=sum(pos.mapped('amount_total'))))
        return True
