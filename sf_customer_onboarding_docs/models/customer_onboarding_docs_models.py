# -*- coding: utf-8 -*-
"""Customer Document Collection models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomerDocReq(models.Model):
    _name = 'sf.customer.doc.req'
    _description = 'Document Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    document_needed = fields.Char(string='Document Needed', required=True)
    needed_for = fields.Selection([
        ('order', 'Order Processing'),
        ('compliance', 'Compliance'),
        ('quality', 'Quality File'),
        ], string='Needed For', required=True, default=order)
    chase_date = fields.Date(string='Chase Date')
    received = fields.Boolean(string='Received')
    blocking_order = fields.Boolean(string='Blocking an Order')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('chased', 'Chased'),
        ('received', 'Received'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.doc.req') or 'NEW'
        return super().create(vals_list)

    def action_chased(self):
        self.write({'state': 'chased'})

    def action_received(self):
        self.write({'state': 'received'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.customer.doc.req'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.customer.doc.req'

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
