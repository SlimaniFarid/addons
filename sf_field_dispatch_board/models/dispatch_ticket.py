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

