# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SfReworkScrap(models.Model):
    _name = 'sf.rework.scrap'
    _description = 'Rework Scrap'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.rework.management.activity.mixin']
    _order = 'id asc'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    order_id = fields.Many2one('sf.rework.order', string='Rework Order',
                               required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, ondelete='restrict')
    qty = fields.Float(string='Quantity', required=True)
    unit_value = fields.Monetary(string='Unit Value', required=True, currency_field='currency_id')
    value = fields.Monetary(string='Value', compute='_compute_value', store=True, currency_field='currency_id')
    scrap_reason = fields.Char(string='Scrap Reason', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_qty_positive', 'CHECK (qty > 0)',
         'The scrap quantity must be greater than zero.'),
    ]

    @api.depends('order_id.name', 'product_id.name')
    def _compute_name(self):
        for scrap in self:
            scrap.name = '%s / %s' % (scrap.order_id.name, scrap.product_id.name)

    @api.depends('qty', 'unit_value')
    def _compute_value(self):
        for scrap in self:
            scrap.value = scrap.qty * scrap.unit_value

    @api.constrains('qty')
    def _check_qty(self):
        for scrap in self:
            if scrap.qty <= 0:
                raise ValidationError(_('The scrap quantity must be greater than zero.'))


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'sf.rework.management.activity.mixin'

    def action_refresh_business(self):
        """Pull on-hand qty and 30-day outbound usage for linked product."""
        for rec in self:
            product = getattr(rec, 'product_id', False)
            if not product:
                continue
            on_hand = product.qty_available
            frm = fields.Date.context_today(rec) - relativedelta(days=30)
            moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('location_dest_id.usage', '=', 'customer'),
                ('date', '>=', frm)])
            usage = sum(m.product_uom.qty for m in moves)
            rec.message_post(body=_(
                'On hand: {h:.2f}; 30-day outbound: {u:.2f} '
                '({m} move(s)).').format(h=on_hand, u=usage, m=len(moves)))
        return True
