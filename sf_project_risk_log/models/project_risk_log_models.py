# -*- coding: utf-8 -*-
"""Project Risk Log models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProjectRisk(models.Model):
    _name = 'sf.project.risk'
    _description = 'Project Risk'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    project_name = fields.Char(string='Project', required=True)
    risk_description = fields.Text(string='Risk Description', required=True)
    probability = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ], string='Probability', required=True, default=medium)
    impact = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ], string='Impact', required=True, default=medium)
    mitigation = fields.Text(string='Mitigation Plan')
    owner_id = fields.Many2one('res.users', string='Risk Owner')
    review_date = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('identified', 'Identified'),
        ('mitigating', 'Mitigating'),
        ('closed', 'Closed'),
        ('occurred', 'Occurred'),
        ], string='Status', default='identified', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.project.risk') or 'NEW'
        return super().create(vals_list)

    def action_mitigating(self):
        self.write({'state': 'mitigating'})

    def action_closed(self):
        self.write({'state': 'closed'})

    def action_occurred(self):
        self.write({'state': 'occurred'})

