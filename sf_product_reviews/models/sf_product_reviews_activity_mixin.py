# -*- coding: utf-8 -*-
from odoo import _, models, api, fields


class SfProductReviewsActivityMixin(models.AbstractModel):
    _name = 'sf.product.reviews.activity.mixin'
    _description = 'Product Reviews Activity Mixin'

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
    _inherit = 'sf.product.review'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('review_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.review_date
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
    _inherit = 'sf.product.review'

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
