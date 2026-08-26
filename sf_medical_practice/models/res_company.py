# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_medical_alert_days = fields.Integer(string='Appointment alert (days)',
                                           default=2)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_medical_alert_days = fields.Integer(
        related='company_id.sf_medical_alert_days', readonly=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.medical.appointment'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

