# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSalonStaff(models.Model):
    _name = 'sf.salon.staff'
    _description = 'Salon Staff'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True, ondelete='restrict')
    commission_rate = fields.Float(string='Commission Rate (%)')
    active = fields.Boolean(string='Active', default=True)
    service_ids = fields.Many2many('sf.salon.service', string='Services')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def _check_rate_edit(self, vals):
        if 'commission_rate' in vals and not self.env.user.has_group('sf_salon_beauty.group_sf_salon_manager'):
            raise UserError(_('Only a salon manager can set commission rates.'))

    def _get_default_commission_rate(self):
        return float(self.env['ir.config_parameter'].sudo().get_param('sf_salon_beauty.default_commission_rate', '10.0'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.salon.staff')
            self._check_rate_edit(vals)
            if 'commission_rate' not in vals:
                vals['commission_rate'] = self._get_default_commission_rate()
        return super().create(vals_list)

    def write(self, vals):
        if 'commission_rate' in vals:
            self._check_rate_edit(vals)
        return super().write(vals)