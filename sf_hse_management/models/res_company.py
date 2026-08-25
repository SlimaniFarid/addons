# -*- coding: utf-8 -*-
from odoo import fields, models, api


class HseResCompany(models.Model):
    _inherit = 'res.company'

    sf_hse_last_major_incident = fields.Datetime(
        string='Last Major/Critical Incident')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.hse.incident'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.due_date
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
                vals['Deadline'] = str(rec.due_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

