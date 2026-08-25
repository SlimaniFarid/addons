# -*- coding: utf-8 -*-
"""Supplier Questionnaire Campaigns models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierQuestionnaire(models.Model):
    _name = 'sf.supplier.questionnaire'
    _description = 'Questionnaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    questionnaire_type = fields.Selection([
        ('compliance', 'Compliance'),
        ('esg', 'ESG'),
        ('quality', 'Quality System'),
        ('cyber', 'Cybersecurity'),
        ], string='Type', required=True)
    sent_date = fields.Date(string='Sent', default=fields.Date.today)
    due_date = fields.Date(string='Response Due')
    score = fields.Float(string='Score (0-100)')
    follow_up = fields.Text(string='Follow-up')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('evaluated', 'Evaluated'),
        ('chased', 'Chased'),
        ], string='Status', default='sent', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.questionnaire') or 'NEW'
        return super().create(vals_list)

    def action_received(self):
        self.write({'state': 'received'})

    def action_evaluated(self):
        self.write({'state': 'evaluated'})

    def action_chased(self):
        self.write({'state': 'chased'})

