# -*- coding: utf-8 -*-
"""Interim Billing Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfInterimBilling(models.Model):
    _name = 'sf.interim.billing'
    _description = 'Interim Billing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    project_ref = fields.Char(string='Project', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    total_contract = fields.Monetary(string='Contract Value', required=True)
    percent_complete = fields.Float(string='% Complete')
    billed_to_date = fields.Monetary(string='Billed to Date')
    next_milestone = fields.Date(string='Next Milestone')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('final_billing', 'Final Billing'),
        ('closed', 'Closed'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.interim.billing') or 'NEW'
        return super().create(vals_list)

    def action_final_billing(self):
        self.write({'state': 'final_billing'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.interim.billing'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.interim.billing'

    def action_refresh_business(self):
        """Pull live sale stats for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            orders = self.env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done'))])
            msg = _('{n} confirmed order(s), total {t:.2f}.').format(
                n=len(orders),
                t=sum(orders.mapped('amount_total')))
            rec.message_post(body=msg)
        return True
