# -*- coding: utf-8 -*-
from odoo import _, fields, models, api


class SfStoreCreditAdjustWizard(models.TransientModel):
    _name = 'sf.store.credit.adjust.wizard'
    _description = 'Store Credit Adjustment'

    credit_id = fields.Many2one('sf.store.credit', string='Credit', required=True)
    amount = fields.Monetary(string='Adjustment Amount', currency_field='currency_id',
                             required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='credit_id.currency_id', readonly=True)
    reason = fields.Char(string='Reason', required=True)

    def action_apply(self):
        self.ensure_one()
        self.credit_id.action_adjust(self.amount, self.reason)
        return {'type': 'ir.actions.act_window_close'}

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.store.credit'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('expiration_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.expiration_date
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.expiration_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.store.credit'

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
