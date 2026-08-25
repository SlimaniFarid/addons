# -*- coding: utf-8 -*-
"""Quality Document Control models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_document_control2(models.Model):
    _name = 'sf.quality_document_control2'
    _description = 'Quality Document Control'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    doc_title = fields.Char(string='Document Title', required=True)
    doc_type = fields.Selection([
        ('sop', 'SOP'),
        ('work_instruction', 'Work Instruction'),
        ('form', 'Form'),
        ('spec', 'Specification'),
        ], string='Type', required=True)
    version = fields.Char(string='Version', default=1.0)
    owner_id = fields.Many2one('res.users', string='Owner')
    review_date = fields.Date(string='Next Review')
    approved_by_id = fields.Many2one('res.users', string='Approved By')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.quality_document_control2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

