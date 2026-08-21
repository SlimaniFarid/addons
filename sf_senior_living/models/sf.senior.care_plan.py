# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSeniorCarePlan(models.Model):
    _name = 'sf.senior.care_plan'
    _description = 'Care Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf_senior_living.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    resident_id = fields.Many2one(string='resident_id', required=True, comodel_name='sf.senior.resident')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    objectives = fields.Html(string='Objectives')
    state = fields.Selection(string='state', default='draft', selection=[('draft', 'Draft'), ('active', 'Active'), ('review', 'Under Review'), ('closed', 'Closed')])
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.senior.care_plan')
            if not vals.get('company_id') and vals.get('resident_id'):
                parent = self.env['sf.senior.resident'].browse(vals['resident_id'])
                vals['company_id'] = parent.company_id.id
        return super().create(vals_list)
