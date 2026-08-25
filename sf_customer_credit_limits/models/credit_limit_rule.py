# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CreditLimitRule(models.Model):
    _name = 'sf.customer.credit.limits.credit.limit.rule'
    _description = 'Credit Limit Rule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    partner_id = fields.Many2one(required=True, comodel_name='res.partner', ondelete='restrict')
    limit_amount = fields.Monetary(string='Limit Amount', required=True, currency_field='currency_id')
    warning_pct = fields.Float(string='Warning Pct', default=80)
    block_over_limit = fields.Boolean(string='Block Over Limit', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.customer.credit.limits.credit.limit.rule') or _('New')
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

