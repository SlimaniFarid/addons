# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SfParkingZone(models.Model):
    _name = 'sf.parking.zone'
    _description = 'Parking Zone'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    site_id = fields.Many2one('sf.parking.site', string='Site', required=True, ondelete='cascade')
    capacity = fields.Integer(string='Capacity', default=0)
    place_ids = fields.One2many('sf.parking.place', 'zone_id', string='Places')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.parking.zone')
            if vals.get('site_id') and not vals.get('company_id'):
                site = self.env['sf.parking.site'].browse(vals['site_id'])
                vals['company_id'] = site.company_id.id
        return super().create(vals_list)

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.parking.activity.mixin'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
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

