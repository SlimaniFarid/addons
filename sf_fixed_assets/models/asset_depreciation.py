# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AssetDepreciation(models.Model):
    _name = 'sf.fixed.asset.depreciation'
    _description = 'Asset Depreciation Line'
    _rec_name = 'asset_id'
    _order = 'period'

    asset_id = fields.Many2one(
        'sf.fixed.asset', string='Asset', required=True,
        ondelete='cascade')
    period = fields.Integer(string='Period (month)', required=True)
    amount = fields.Monetary(string='Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    currency_id = fields.Many2one(
        related='asset_id.currency_id', string='Currency', readonly=True)
    posted = fields.Boolean(string='Posted', default=False)

    @api.constrains('amount')
    def _check_amount(self):
        for line in self:
            if line.amount < 0:
                raise models.ValidationError(
                    _('Depreciation amount must be positive.'))


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.fixed.asset'

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
