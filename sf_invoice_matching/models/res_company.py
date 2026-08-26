# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_match_tolerance_qty = fields.Float(
        string='Qty tolerance', default=0.0)
    sf_match_tolerance_price_pct = fields.Float(
        string='Price tolerance (%)', default=2.0)
    sf_match_tolerance_total_pct = fields.Float(
        string='Total tolerance (%)', default=2.0)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sf_match_tolerance_qty = fields.Float(
        string='Supplier qty tolerance', default=-1.0,
        help='Specific tolerance for this supplier. -1 means use the '
             'company default.')
    sf_match_tolerance_price_pct = fields.Float(
        string='Supplier price tolerance (%)', default=-1.0,
        help='Specific tolerance for this supplier. -1 means use the '
             'company default.')
    sf_match_tolerance_total_pct = fields.Float(
        string='Supplier total tolerance (%)', default=-1.0,
        help='Specific tolerance for this supplier. -1 means use the '
             'company default.')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_match_tolerance_qty = fields.Float(
        related='company_id.sf_match_tolerance_qty', readonly=False)
    sf_match_tolerance_price_pct = fields.Float(
        related='company_id.sf_match_tolerance_price_pct', readonly=False)
    sf_match_tolerance_total_pct = fields.Float(
        related='company_id.sf_match_tolerance_total_pct', readonly=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.invoice.match.line'

    active = fields.Boolean(string='Active', default=True)
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.invoice.match.line'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
