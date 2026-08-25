# -*- coding: utf-8 -*-
"""OEE Calculator models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProduction_oee_calculator(models.Model):
    _name = 'sf.production_oee_calculator'
    _description = 'OEE Calculator'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center', required=True)
    period = fields.Char(string='Period', required=True)
    planned_time = fields.Float(string='Planned Time (min)')
    downtime = fields.Float(string='Downtime (min)')
    ideal_cycle = fields.Float(string='Ideal Cycle (s)')
    total_count = fields.Integer(string='Total Count')
    good_count = fields.Integer(string='Good Count')
    oee_percent = fields.Float(string='OEE %')
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
                    'sf.production_oee_calculator') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

