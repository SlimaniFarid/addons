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

    plan_id = fields.Many2one(comodel_name='sf.preventive.maintenance.pro.pm.plan', ondelete='restrict')
    maintenance_request_id = fields.Many2one(comodel_name='maintenance.request', ondelete='restrict')
    created_date = fields.Date(string='Created Date', default=fields.Date.today)
    state = fields.Selection([
        ('pending', 'Pending'), ('in_progress', 'In Progress'),
        ('done', 'Done'), ('cancelled', 'Cancelled'),
        ], string='Status', default='pending', copy=False)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.preventive.maintenance.pro.pm.plan'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('next_due', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.next_due
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

    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.next_due)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

