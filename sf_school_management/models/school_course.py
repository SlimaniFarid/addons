# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolCourse(models.Model):
    _name = 'sf.school.course'
    _description = 'School Course'
    _order = 'name'

    name = fields.Char(string='Course', required=True, index=True)
    subject = fields.Char(string='Subject')
    teacher_id = fields.Many2one('sf.school.teacher', string='Teacher',
                                 ondelete='restrict')
    group_ids = fields.Many2many('sf.school.group', string='Groups')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.school.course')
        return super().create(vals)