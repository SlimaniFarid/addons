# -*- coding: utf-8 -*-
"""Customer Segmentation Rules models"""
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_segments_rules(models.Model):
    _name = 'sf.customer_segments_rules'
    _description = 'Customer Segmentation Rules'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    segment_name = fields.Char(string='Segment Name', required=True)
    recency_max_days = fields.Integer(string='Max Days Since Last Order')
    frequency_min = fields.Integer(string='Min Orders')
    monetary_min = fields.Monetary(string='Min Total Revenue')
    member_count = fields.Integer(string='Members')
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
                    'sf.customer_segments_rules') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.customer_segments_rules'

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


# --- wave2 ---
class _Wave2(models.Model):
    _inherit = 'sf.customer_segments_rules'

    def action_refresh_members(self):
        """Real RFM: members matching recency/frequency/monetary filters,
        computed from confirmed customer orders."""
        Sale = self.env['sale.order']
        self.ensure_one()
        domain = [('state', 'in', ('sale', 'done')),
                  ('company_id', '=', self.company_id.id)]
        if self.recency_max_days:
            limit = fields.Date.context_today(self) - relativedelta(
                days=self.recency_max_days)
            domain.append(('date_order', '>=', limit))
        groups = Sale._read_group(
            domain, ['partner_id'], aggregates=['id:count', 'amount_total:sum'])
        count = 0
        for partner, order_count, total in groups:
            if order_count >= (self.frequency_min or 0)                     and total >= (self.monetary_min or 0.0):
                count += 1
        self.member_count = count
        self.message_post(body=_(
            'RFM refresh: %(c)s member(s) match '
            '(recency<=%(r)s d, orders>=%(f)s, revenue>=%(m)s).') % {
                'c': count, 'r': self.recency_max_days or '∞',
                'f': self.frequency_min or 0, 'm': self.monetary_min or 0})
        return True
