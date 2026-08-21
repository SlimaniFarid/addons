# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSeniorResidence(models.Model):
    _name = 'sf.senior.residence'
    _description = 'Senior Residence'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf_senior_living.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    address = fields.Text(string='Address')
    capacity = fields.Integer(string='Capacity')
    state = fields.Selection(string='state', default='active', selection=[('active', 'Active'), ('maintenance', 'Maintenance'), ('closed', 'Closed')])
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.senior.residence')
            if not vals.get('company_id') and vals.get('residence_id'):
                parent = self.env['sf.senior.residence'].browse(vals['residence_id'])
                vals['company_id'] = parent.company_id.id
        return super().create(vals_list)
