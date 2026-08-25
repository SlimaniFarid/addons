# -*- coding: utf-8 -*-
"""Customer Visit Reports models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVisitReport(models.Model):
    _name = 'sf.visit.report'
    _description = 'Visit Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    visit_date = fields.Date(string='Visit Date', required=True, default=fields.Date.today)
    visited_by_id = fields.Many2one('res.users', string='Visited By')
    agenda = fields.Text(string='Agenda')
    findings = fields.Html(string='Findings')
    opportunities = fields.Html(string='Opportunities Spotted')
    next_steps = fields.Text(string='Next Steps')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.visit.report') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_acknowledged(self):
        self.write({'state': 'acknowledged'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.visit.report'

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

