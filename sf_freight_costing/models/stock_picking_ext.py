# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockPickingFreight(models.Model):
    _inherit = 'stock.picking'

    sf_carrier_id = fields.Many2one('sf.freight.carrier', string='Carrier')
    sf_freight_cost_ids = fields.One2many('sf.freight.cost', 'picking_id',
                                          string='Freight Costs')
    sf_weight = fields.Float(string='Weight (kg)', compute='_compute_freight')
    sf_volume = fields.Float(string='Volume (m3)', compute='_compute_freight')
    sf_estimated_freight = fields.Float(string='Estimated Freight',
                                        compute='_compute_freight')

    @api.depends('move_ids.product_uom_qty', 'move_ids.product_id.weight',
                 'sf_carrier_id', 'move_ids.product_id.volume')
    def _compute_freight(self):
        for picking in self:
            weight = 0.0
            volume = 0.0
            value = 0.0
            for move in picking.move_ids:
                weight += (move.product_id.weight or 0.0) * move.product_uom_qty
                volume += (move.product_id.volume or 0.0) * move.product_uom_qty
                value += (move.product_id.lst_price or 0.0) * move.product_uom_qty
            picking.sf_weight = weight
            picking.sf_volume = volume
            est = 0.0
            if picking.sf_carrier_id:
                est = self.env['sf.freight.carrier'].compute_cost(
                    picking.sf_carrier_id, weight, volume, value)
            picking.sf_estimated_freight = est


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.freight.carrier'

    def action_refresh_business(self):
        """Pull open / overdue amounts for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            moves = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('partner_id', '=', partner.id)])
            open_amt = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
            ).mapped('amount_residual'))
            today = fields.Date.context_today(rec)
            overdue = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
                and m.invoice_date_due
                and m.invoice_date_due < today
            ).mapped('amount_residual'))
            rec.message_post(body=_(
                'Open: {o:.2f}, Overdue: {d:.2f} '
                '({c} posted invoice(s)).').format(
                o=open_amt, d=overdue, c=len(moves)))
        return True
