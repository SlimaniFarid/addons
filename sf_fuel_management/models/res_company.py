# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_fuel_alert_days = fields.Integer(
        string='Fuel card expiry alert (days)', default=7)
    sf_fuel_max_l100 = fields.Float(
        string='Max consumption alert (L/100km)', default=12.0)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_fuel_alert_days = fields.Integer(
        related='company_id.sf_fuel_alert_days', readonly=False)
    sf_fuel_max_l100 = fields.Float(
        related='company_id.sf_fuel_max_l100', readonly=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.fuel.vehicle'

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

    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.expiry_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

