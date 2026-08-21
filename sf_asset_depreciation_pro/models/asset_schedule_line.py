# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AssetScheduleLine(models.Model):
    _name = 'sf.asset.depreciation.pro.asset.schedule.line'
    _description = 'Asset Schedule Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    asset_id = fields.Many2one(comodel_name='account.asset', ondelete='restrict')
    depreciation_date = fields.Date(string='Depreciation Date')
    amount = fields.Monetary(string='Amount', currency_field='currency_id', currency_field='currency_id')
    posted = fields.Boolean(string='Posted', default='False')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.asset.depreciation.pro.asset.schedule.line') or _('New')
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

