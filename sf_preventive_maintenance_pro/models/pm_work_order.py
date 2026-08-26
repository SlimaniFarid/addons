# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PmWorkOrder(models.Model):
    _name = 'sf.preventive.maintenance.pro.pm.work.order'
    _description = 'Pm Work Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    plan_id = fields.pm.plan(string='Plan Id')
    maintenance_request_id = fields.maintenance.request(string='Maintenance Request Id')
    created_date = fields.Created(string='Created Date', default=fields.Date.today)
    state = fields.pending,created,done(string='State', default='pending')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.preventive.maintenance.pro.pm.plan'

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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.preventive.maintenance.pro.pm.plan'

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
