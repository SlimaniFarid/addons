# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ComplianceResCompany(models.Model):
    _inherit = 'res.company'

    sf_compliance_default_alert_days = fields.Integer(
        string='Default Alert Days', default=30)
    sf_compliance_require_attachment = fields.Boolean(
        string='Require Attachment at Publication', default=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.compliance.document.type'

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

