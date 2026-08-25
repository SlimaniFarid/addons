# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_oh_alert_days = fields.Integer(
        string='Medical validity alert (days)', default=30)
    sf_oh_auto_create_periodic = fields.Boolean(
        string='Auto-create periodic visits', default=False)
    sf_oh_default_interval_months = fields.Integer(
        string='Default visit periodicity (months)', default=12)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_oh_alert_days = fields.Integer(
        related='company_id.sf_oh_alert_days', readonly=False)
    sf_oh_auto_create_periodic = fields.Boolean(
        related='company_id.sf_oh_auto_create_periodic', readonly=False)
    sf_oh_default_interval_months = fields.Integer(
        related='company_id.sf_oh_default_interval_months', readonly=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.oh.medical.file'

    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('next_due_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.next_due_date
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
                vals['Deadline'] = str(rec.next_due_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

