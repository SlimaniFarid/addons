# -*- coding: utf-8 -*-
"""Batch Job Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBatch_job_monitor(models.Model):
    _name = 'sf.batch_job_monitor'
    _description = 'Batch Job Monitor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    job_name = fields.Char(string='Job Name', required=True)
    last_run = fields.Datetime(string='Last Run')
    duration_seconds = fields.Float(string='Duration (s)')
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('timeout', 'Timeout'),
        ], string='Status', required=True)
    records_processed = fields.Integer(string='Records')
    error_detail = fields.Text(string='Error Detail')
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
                    'sf.batch_job_monitor') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

