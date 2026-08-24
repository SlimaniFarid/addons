# -*- coding: utf-8 -*-
"""Safety Training Compliance models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSafety_training_tracker(models.Model):
    _name = 'sf.safety_training_tracker'
    _description = 'Safety Training Compliance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    training_type = fields.Selection([
        ('fire', 'Fire Safety'),
        ('first_aid', 'First Aid'),
        ('forklift', 'Forklift'),
        ('chemical', 'Chemical Handling'),
        ('other', 'Other'),
        ], string='Training', required=True)
    completed_date = fields.Date(string='Completed')
    expiry_date = fields.Date(string='Expiry')
    compliant = fields.Boolean(string='Compliant')
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
                    'sf.safety_training_tracker') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

