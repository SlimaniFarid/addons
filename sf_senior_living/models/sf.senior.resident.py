# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSeniorResident(models.Model):
    _name = 'sf.senior.resident'
    _description = 'Senior Resident'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf_senior_living.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    residence_id = fields.Many2one(string='residence_id', required=True, comodel_name='sf.senior.residence')
    date_of_birth = fields.Date(string='Date of Birth')
    gir_level = fields.Selection(string='gir_level', selection=[('1', 'GIR 1'), ('2', 'GIR 2'), ('3', 'GIR 3'), ('4', 'GIR 4'), ('5', 'GIR 5'), ('6', 'GIR 6')])
    state = fields.Selection(string='state', default='admitted', selection=[('admitted', 'Admitted'), ('discharged', 'Discharged'), ('deceased', 'Deceased')])
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.senior.resident')
            if not vals.get('company_id') and vals.get('residence_id'):
                parent = self.env['sf.senior.residence'].browse(vals['residence_id'])
                vals['company_id'] = parent.company_id.id
        return super().create(vals_list)
