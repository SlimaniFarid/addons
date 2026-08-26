# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DispatchTicket(models.Model):
    _name = 'sf.field.dispatch.board.dispatch.ticket'
    _description = 'Dispatch Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    name = fields.Ticket(string='Name', required=True)
    partner_id = fields.res.partner(string='Partner Id', required=True)
    technician_id = fields.res.users(string='Technician Id')
    priority = fields.low,normal,high,urgent(string='Priority', default='normal')
    scheduled_date = fields.Scheduled(string='Scheduled Date')
    state = fields.new,assigned,en_route,in_progress,done,cancelled(string='State', default='new tracking', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.field.dispatch.board.dispatch.ticket') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.state not in ('draft',):
                raise UserError(_('Only draft records can be confirmed.'))
            rec.state = rec._get_next_state()
    
    def _get_next_state(self):
        states = [s[0] for s in self._fields['state'].selection]
        idx = states.index(self.state)
        return states[min(idx + 1, len(states) - 1)]

    def action_cancel(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.field.dispatch.board.dispatch.ticket'

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
    _inherit = 'sf.field.dispatch.board.dispatch.ticket'

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
