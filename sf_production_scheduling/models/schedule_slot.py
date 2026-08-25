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

    plan_id = fields.Many2one(required=True, comodel_name='sf.production.scheduling.schedule.plan', ondelete='restrict')
    mo_id = fields.Many2one(comodel_name='mrp.production', ondelete='restrict')
    start_datetime = fields.Datetime(string='Start Datetime')
    end_datetime = fields.Datetime(string='End Datetime')
    workcenter_id = fields.Many2one(comodel_name='mrp.workcenter', ondelete='restrict')

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

