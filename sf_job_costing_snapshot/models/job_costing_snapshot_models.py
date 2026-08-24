# -*- coding: utf-8 -*-
"""Job Costing Snapshot models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfJobCost(models.Model):
    _name = 'sf.job.cost'
    _description = 'Job Cost Snapshot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    job_name = fields.Char(string='Job / Project', required=True)
    snapshot_date = fields.Date(string='Snapshot', default=fields.Date.today)
    labor_cost = fields.Monetary(string='Labor')
    material_cost = fields.Monetary(string='Materials')
    overhead_cost = fields.Monetary(string='Overheads')
    budget_total = fields.Monetary(string='Budget')
    margin_percent = fields.Float(string='Margin %')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.job.cost') or 'NEW'
        return super().create(vals_list)

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

