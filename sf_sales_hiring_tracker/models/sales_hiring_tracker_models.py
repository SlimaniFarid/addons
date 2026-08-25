# -*- coding: utf-8 -*-
"""Sales Hiring & Ramp Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_hiring_tracker(models.Model):
    _name = 'sf.sales_hiring_tracker'
    _description = 'Sales Hiring & Ramp Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    candidate_name = fields.Char(string='Candidate', required=True)
    stage = fields.Selection([
        ('sourcing', 'Sourcing'),
        ('interviewing', 'Interviewing'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('ramping', 'Ramping'),
        ('productive', 'Productive'),
        ], string='Stage', required=True)
    start_date = fields.Date(string='Start Date')
    ramp_end_date = fields.Date(string='Ramp End')
    quota_attainment = fields.Float(string='Quota Attainment %')
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
                    'sf.sales_hiring_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

