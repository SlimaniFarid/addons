# -*- coding: utf-8 -*-
from odoo import fields, models, api


class OnboardingResCompany(models.Model):
    _inherit = 'res.company'

    sf_onboarding_default_template = fields.Many2one(
        'sf.onboarding.template', string='Default Onboarding Template')
    sf_offboarding_default_template = fields.Many2one(
        'sf.onboarding.template', string='Default Offboarding Template')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.onboarding.template'

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

