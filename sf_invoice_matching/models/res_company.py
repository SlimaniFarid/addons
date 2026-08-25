# -*- coding: utf-8 -*-
from odoo import fields, models


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

