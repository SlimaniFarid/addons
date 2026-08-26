# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class RequisitionLine(models.Model):
    _name = 'sf.purchase.requisition.requisition.line'
    _description = 'Requisition Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    requisition_id = fields.Many2one(comodel_name='purchase.requisition.sf', ondelete='restrict')
    product_id = fields.Many2one(required=True, comodel_name='product.product', ondelete='restrict')
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    price_estimated = fields.Monetary(string='Price Estimated', currency_field='currency_id')
    vendor_suggested = fields.Many2one(comodel_name='res.partner', ondelete='restrict')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.purchase.requisition.purchase.requisition.sf'

    active = fields.Boolean(string='Active', default=True)
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


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'sf.purchase.requisition.purchase.requisition.sf'

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
