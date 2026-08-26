# -*- coding: utf-8 -*-
"""Revenue Backlog Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRevenueBacklog(models.Model):
    _name = 'sf.revenue.backlog'
    _description = 'Backlog Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    contract_ref = fields.Char(string='Contract / Order Ref', required=True)
    backlog_amount = fields.Monetary(string='Backlog Amount', required=True)
    expected_invoice_month = fields.Date(string='Expected Invoice Month')
    invoiced_amount = fields.Float(string='Invoiced So Far')
    risk_note = fields.Text(string='Risk Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('partially_invoiced', 'Partially Invoiced'),
        ('invoiced', 'Invoiced'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.revenue.backlog') or 'NEW'
        return super().create(vals_list)

    def action_partially_invoiced(self):
        self.write({'state': 'partially_invoiced'})

    def action_invoiced(self):
        self.write({'state': 'invoiced'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.revenue.backlog'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.revenue.backlog'

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
