# -*- coding: utf-8 -*-
"""Escalation Rules Engine models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_escalation_rules(models.Model):
    _name = 'sf.customer_care_escalation_rules'
    _description = 'Escalation Rules Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rule_name = fields.Char(string='Rule Name', required=True)
    trigger = fields.Selection([
        ('sla_breach', 'SLA Breach'),
        ('severity', 'Severity Increase'),
        ('customer_tier', 'Customer Tier'),
        ('repeat_issue', 'Repeat Issue'),
        ], string='Trigger', required=True)
    tier = fields.Integer(string='Escalation Tier', required=True)
    escalate_to_id = fields.Many2one('res.users', string='Escalate To', required=True)
    timer_minutes = fields.Integer(string='Timer (min)')
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
                    'sf.customer_care_escalation_rules') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.customer_care_escalation_rules'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_submitted(self):
        res = super().action_submitted()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

