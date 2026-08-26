# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolGroup(models.Model):
    _name = 'sf.school.group'
    _description = 'School Group / Class'
    _order = 'name'

    name = fields.Char(string='Group', required=True, index=True)
    year_id = fields.Many2one('sf.school.year', string='School year',
                              required=True, ondelete='restrict', index=True)
    level = fields.Char(string='Level')
    supervisor_id = fields.Many2one('sf.school.teacher',
                                    string='Supervisor', ondelete='restrict')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.group')
        return super().create(vals)