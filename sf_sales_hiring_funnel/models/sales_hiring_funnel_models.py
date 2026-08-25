# -*- coding: utf-8 -*-
"""Sales Hiring Funnel models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_hiring_funnel(models.Model):
    _name = 'sf.sales_hiring_funnel'
    _description = 'Sales Hiring Funnel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    position = fields.Char(string='Position', required=True)
    stage = fields.Selection([
        ('sourcing', 'Sourcing'),
        ('screening', 'Screening'),
        ('interviewing', 'Interviewing'),
        ('offer', 'Offer Extended'),
        ('hired', 'Hired'),
        ], string='Stage', required=True)
    candidate_count = fields.Integer(string='Candidates')
    target_start_date = fields.Date(string='Target Start')
    hiring_manager_id = fields.Many2one('res.users', string='Hiring Manager')
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
                    'sf.sales_hiring_funnel') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

