# -*- coding: utf-8 -*-
"""Shift Handover Notes (Workcenters) models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfShiftHandover(models.Model):
    _name = 'sf.shift.handover'
    _description = 'Shift Handover'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center', required=True)
    shift = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
        ], string='Shift', required=True)
    handover_date = fields.Date(string='Date', required=True, default=fields.Date.today)
    running_orders = fields.Text(string='Running Orders')
    issues = fields.Text(string='Open Issues')
    watchouts = fields.Text(string='Watch-outs for Next Shift')
    operator_id = fields.Many2one('res.users', string='Handover By')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('acknowledged', 'Acknowledged by Next Shift'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.shift.handover') or 'NEW'
        return super().create(vals_list)

    def action_acknowledged(self):
        self.write({'state': 'acknowledged'})

