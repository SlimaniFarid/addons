# -*- coding: utf-8 -*-
from odoo import _, api, models, fields
from dateutil.relativedelta import relativedelta


class SfAqlSamplingActivityMixin(models.AbstractModel):
    _name = 'sf.aql.sampling.activity.mixin'
    _description = 'AQL Sampling Activity Mixin'

    def _sf_check_todo(self, todo_type, subject, note=None):
        self.ensure_one()
        existing = self.activity_ids.filtered(
            lambda a: a.activity_type_id == todo_type
            and a.summary == subject
            and not a.done
        )
        if existing:
            return existing[0]
        return self.activity_schedule(
            todo_type,
            summary=subject,
            note=note,
        )

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.aql.defect'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _WaveFinalStock(models.Model):
    _inherit = 'sf.aql.defect'

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
