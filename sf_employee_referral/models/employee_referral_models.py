# -*- coding: utf-8 -*-
"""Employee Referral Program models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfReferral(models.Model):
    _name = 'sf.referral'
    _description = 'Referral'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    referrer_id = fields.Many2one('hr.employee', string='Referring Employee', required=True)
    candidate_name = fields.Char(string='Candidate', required=True)
    position = fields.Char(string='Position')
    hired = fields.Boolean(string='Hired')
    hire_date = fields.Date(string='Hire Date')
    bonus_amount = fields.Monetary(string='Referral Bonus')
    bonus_paid = fields.Boolean(string='Bonus Paid')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('referred', 'Referred'),
        ('interviewing', 'Interviewing'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ], string='Status', default='referred', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.referral') or 'NEW'
        return super().create(vals_list)

    def action_interviewing(self):
        self.write({'state': 'interviewing'})

    def action_hired(self):
        self.write({'state': 'hired'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

