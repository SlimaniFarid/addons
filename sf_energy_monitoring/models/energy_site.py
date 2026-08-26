# -*- coding: utf-8 -*-
from odoo import fields, models


class EnergySite(models.Model):
    _name = 'sf.energy.site'
    _description = 'Energy Site'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    address = fields.Text(string='Address')
    meter_ids = fields.One2many('sf.energy.meter', 'site_id',
                                string='Meters')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.energy.meter'

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

