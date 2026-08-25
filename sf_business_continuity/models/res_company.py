# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_bcp_review_days = fields.Integer(
        string='BCP plan review interval (days)', default=365)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_bcp_review_days = fields.Integer(
        related='company_id.sf_bcp_review_days', readonly=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.bcp.process'

    active = fields.Boolean(string='Active', default=True)
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('last_review_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.last_review_date
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
                vals['Deadline'] = str(rec.last_review_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

