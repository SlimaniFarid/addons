# -*- coding: utf-8 -*-
"""Probation Review Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProbationReview(models.Model):
    _name = 'sf.probation.review'
    _description = 'Probation Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    probation_end = fields.Date(string='Probation End', required=True)
    review_1_date = fields.Date(string='Mid Review')
    review_2_date = fields.Date(string='Final Review')
    outcome = fields.Selection([
        ('confirm', 'Confirm'),
        ('extend', 'Extend'),
        ('terminate', 'Terminate'),
        ], string='Outcome')
    manager_comments = fields.Text(string='Manager Comments')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('in_probation', 'In Probation'),
        ('review_scheduled', 'Review Scheduled'),
        ('confirmed', 'Confirmed'),
        ('extended', 'Extended'),
        ('terminated', 'Terminated'),
        ], string='Status', default='in_probation', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.probation.review') or 'NEW'
        return super().create(vals_list)

    def action_review_scheduled(self):
        self.write({'state': 'review_scheduled'})

    def action_confirmed(self):
        self.write({'state': 'confirmed'})

    def action_extended(self):
        self.write({'state': 'extended'})

    def action_terminated(self):
        self.write({'state': 'terminated'})

