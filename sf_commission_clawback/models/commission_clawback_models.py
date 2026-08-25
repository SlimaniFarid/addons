# -*- coding: utf-8 -*-
"""Sales Commission Clawback models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfClawback(models.Model):
    _name = 'sf.clawback'
    _description = 'Clawback Case'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', required=True)
    reason = fields.Selection([
        ('return', 'Product Return'),
        ('non_payment', 'Non-Payment'),
        ('cancellation', 'Cancellation'),
        ], string='Reason', required=True)
    commission_amount = fields.Monetary(string='Commission to Recover', required=True)
    recovered_amount = fields.Float(string='Recovered')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('notified', 'Notified'),
        ('recovered', 'Recovered'),
        ('written_off', 'Written Off'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.clawback') or 'NEW'
        return super().create(vals_list)

    def action_notified(self):
        self.write({'state': 'notified'})

    def action_recovered(self):
        self.write({'state': 'recovered'})

    def action_written_off(self):
        self.write({'state': 'written_off'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.clawback'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
