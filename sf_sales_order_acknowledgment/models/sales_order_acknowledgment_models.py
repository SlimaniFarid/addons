# -*- coding: utf-8 -*-
"""Order Acknowledgment Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfOrderAck(models.Model):
    _name = 'sf.order.ack'
    _description = 'Order Acknowledgment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    customer_requires = fields.Boolean(string='Customer Requires OA', default=True)
    sent_date = fields.Date(string='OA Sent')
    customer_signed = fields.Boolean(string='Customer Signed')
    chase_date = fields.Date(string='Chase Date')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('signed', 'Signed'),
        ('chased', 'Chased'),
        ], string='Status', default='pending', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.order.ack') or 'NEW'
        return super().create(vals_list)

    def action_sent(self):
        self.write({'state': 'sent'})

    def action_signed(self):
        self.write({'state': 'signed'})

    def action_chased(self):
        self.write({'state': 'chased'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.order.ack'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.order.ack'

    def action_refresh_business(self):
        """Post a status summary to chatter (generic)."""
        for rec in self:
            parts = []
            for fname in ('state', 'user_id', 'company_id'):
                val = getattr(rec, fname, False)
                if val:
                    parts.append('{0}: {1}'.format(
                        fname, val.display_name if hasattr(val, 'display_name')
                        else val))
            rec.message_post(body=' | '.join(parts) or 'No data.')
        return True
