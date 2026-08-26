# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ScheduleSlot(models.Model):
    _name = 'sf.production.scheduling.schedule.slot'
    _description = 'Schedule Slot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    plan_id = fields.schedule.plan(string='Plan Id', required=True)
    mo_id = fields.mrp.production(string='Mo Id')
    start_datetime = fields.Start(string='Start Datetime')
    end_datetime = fields.End(string='End Datetime')
    workcenter_id = fields.mrp.workcenter(string='Workcenter Id')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.production.scheduling.schedule.plan'

    active = fields.Boolean(string='Active', default=True)
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
    _inherit = 'sf.production.scheduling.schedule.plan'

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
