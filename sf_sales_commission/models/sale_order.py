# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commission_line_ids = fields.One2many(
        'sf.commission.line',
        'sale_order_id',
        string='Commission Lines',
        readonly=True,
    )
    total_commission = fields.Monetary(
        string='Total Commission',
        compute='_compute_total_commission',
        store=True,
    )

    @api.depends('commission_line_ids.final_commission')
    def _compute_total_commission(self):
        for order in self:
            order.total_commission = sum(
                order.commission_line_ids.mapped('final_commission'))

    def action_generate_commission(self):
        """Generate commission lines for the given confirmed sale orders."""
        for order in self:
            if order.state not in ('sale', 'done'):
                continue
            if order.commission_line_ids:
                continue
            plan = self.env['sf.commission.plan'].search([
                ('active', '=', True),
                ('company_id', '=', order.company_id.id),
            ], order='sequence asc, id asc', limit=1)
            if not plan:
                continue
            salesperson = order.user_id or order.partner_id.user_id
            if not salesperson:
                continue
            base = order.amount_total
            if plan.calculation_type == 'margin':
                margin = order.amount_total - sum(
                    line.price_cost * line.product_uom_qty
                    for line in order.order_line if line.product_id)
                if margin <= 0:
                    continue
                base = margin
            self.env['sf.commission.line'].create({
                'name': order.name,
                'date': order.date_order.date() if order.date_order
                else fields.Date.context_today(self),
                'salesperson_id': salesperson.id,
                'plan_id': plan.id,
                'sale_order_id': order.id,
                'base_amount': base,
                'rate': plan.rate,
                'state': 'draft',
            })
        return True

    def action_view_commission_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Commission Lines',
            'res_model': 'sf.commission.line',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id},
        }


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.commission.plan'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
