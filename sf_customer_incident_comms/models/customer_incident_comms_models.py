# -*- coding: utf-8 -*-
"""Customer Incident Communications models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomerComm(models.Model):
    _name = 'sf.customer.comm'
    _description = 'Customer Communication'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    incident_ref = fields.Char(string='Incident Reference', required=True)
    channel = fields.Selection([
        ('email', 'Email'),
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ], string='Channel', default=email)
    message_sent = fields.Html(string='Message Sent')
    sent_at = fields.Datetime(string='Sent At', default=fields.Datetime.now)
    customer_reaction = fields.Text(string='Customer Reaction')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('sent', 'Sent'),
        ('feedback', 'Feedback Received'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.comm') or 'NEW'
        return super().create(vals_list)

    def action_sent(self):
        self.write({'state': 'sent'})

    def action_feedback(self):
        self.write({'state': 'feedback'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.customer.comm'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.customer.comm'

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
