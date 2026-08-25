# -*- coding: utf-8 -*-
"""Internship Program Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfInternship_tracker(models.Model):
    _name = 'sf.internship_tracker'
    _description = 'Internship Program Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    intern_name = fields.Char(string='Intern Name', required=True)
    school = fields.Char(string='School / University')
    start_date = fields.Date(string='Start', required=True)
    end_date = fields.Date(string='End')
    mentor_id = fields.Many2one('hr.employee', string='Mentor')
    conversion_status = fields.Selection([
        ('pending', 'Pending'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ], string='Conversion', default=pending)
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
                    'sf.internship_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

