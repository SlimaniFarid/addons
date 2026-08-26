# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfStaffingClient(models.Model):
    _name = 'sf.staffing.client'
    _description = 'Staffing Client'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner')
    contact_name = fields.Char(string='Contact Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)
    need_ids = fields.One2many('sf.staffing.need', 'client_id', string='Needs')
    mission_ids = fields.One2many('sf.staffing.mission', 'client_id', string='Missions')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.staffing.client')
        return super().create(vals_list)