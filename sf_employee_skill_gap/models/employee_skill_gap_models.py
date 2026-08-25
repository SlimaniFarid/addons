# -*- coding: utf-8 -*-
"""Employee Skill Gap Analyzer models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfEmployee_skill_gap(models.Model):
    _name = 'sf.employee_skill_gap'
    _description = 'Employee Skill Gap Analyzer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    role = fields.Char(string='Role', required=True)
    required_skills = fields.Text(string='Required Skills')
    actual_skills = fields.Text(string='Actual Skills')
    gap_analysis = fields.Html(string='Gap Analysis')
    training_plan = fields.Text(string='Training Plan')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.employee_skill_gap') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

