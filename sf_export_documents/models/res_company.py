# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_export_origin_country_id = fields.Many2one(
        'res.country', string='Default country of origin')
    sf_export_alert_days = fields.Integer(
        string='Export preparation alert (days)', default=3)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_export_origin_country_id = fields.Many2one(
        'res.country', related='company_id.sf_export_origin_country_id',
        readonly=False)
    sf_export_alert_days = fields.Integer(
        related='company_id.sf_export_alert_days', readonly=False)


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.export.incoterm'

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
