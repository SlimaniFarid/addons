# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PsaTimeEntry(models.Model):
    _name = 'sf.psa.time.entry'
    _description = 'PSA Time Entry'
    _order = 'date desc'

    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    engagement_id = fields.Many2one('sf.psa.engagement', string='Engagement',
                                    required=True)
    assignment_id = fields.Many2one('sf.psa.assignment', string='Assignment',
                                    ondelete='cascade')
    resource_id = fields.Many2one('sf.psa.resource', string='Resource',
                                  required=True)
    hours = fields.Float(string='Hours', required=True, default=1.0)
    description = fields.Text(string='Description')
    billable = fields.Boolean(string='Billable', default=True)
    amount = fields.Float(string='Amount', compute='_compute_amount',
                          store=True)

    @api.depends('hours', 'resource_id.hourly_rate', 'billable')
    def _compute_amount(self):
        for entry in self:
            rate = entry.resource_id.hourly_rate or 0.0
            entry.amount = (entry.hours * rate) if entry.billable else 0.0

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.psa.assignment'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
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
    _inherit = 'sf.psa.assignment'

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
