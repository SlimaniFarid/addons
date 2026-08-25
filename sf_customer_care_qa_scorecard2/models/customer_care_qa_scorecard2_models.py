# -*- coding: utf-8 -*-
"""QA Scorecard models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_qa_scorecard2(models.Model):
    _name = 'sf.customer_care_qa_scorecard2'
    _description = 'QA Scorecard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    agent_id = fields.Many2one('res.users', string='Agent', required=True)
    interaction_ref = fields.Char(string='Interaction Ref', required=True)
    qa_score = fields.Float(string='QA Score (0-100)')
    strengths = fields.Text(string='Strengths')
    improvements = fields.Text(string='Improvement Areas')
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer_care_qa_scorecard2') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

