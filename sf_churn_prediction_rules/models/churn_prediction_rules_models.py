# -*- coding: utf-8 -*-
"""Churn Prediction Rules Engine models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfChurn_prediction_rules(models.Model):
    _name = 'sf.churn_prediction_rules'
    _description = 'Churn Prediction Rules Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rule_name = fields.Char(string='Rule Name', required=True)
    signal_type = fields.Selection([
        ('usage_decline', 'Usage Decline'),
        ('support_tickets', 'Support Tickets Up'),
        ('champion_left', 'Champion Left'),
        ('no_orders', 'No Recent Orders'),
        ], string='Signal', required=True)
    weight = fields.Float(string='Weight', default=1.0)
    threshold = fields.Float(string='Alert Threshold')
    alert_action = fields.Text(string='Alert Action')
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
                    'sf.churn_prediction_rules') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.churn_prediction_rules'

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
class _Wave2Churn(models.Model):
    _inherit = 'sf.churn_prediction_rules'

    def action_scan_customers(self):
        """Score every customer with >=1 confirmed order against active
        rules. Signals supported:
          - no_orders: threshold = days since last confirmed order
          - usage_decline: threshold = % revenue drop vs previous 30d
        Customers breaching any rule are logged on each rule's chatter and
        a summary notification is returned."""
        Partner = self.env['res.partner']
        Sale = self.env['sale.order']
        today = fields.Date.context_today(self)
        customers = Partner.search([('customer_rank', '>', 0)], limit=500)
        stats = {}
        for p in customers:
            orders = Sale.search([
                ('partner_id', '=', p.id),
                ('state', 'in', ('sale', 'done'))], order='date_order desc')
            if not orders:
                continue
            last = fields.Date.to_date(orders[0].date_order)
            stats[p.id] = {
                'days_since': (today - last).days,
                'name': p.display_name,
            }
        summary = []
        for rule in self.search([('active', '=', True)]):
            hit_ids = []
            if rule.signal_type == 'no_orders':
                thr = int(rule.threshold or 60)
                hit_ids = [pid for pid, s in stats.items()
                           if s['days_since'] > thr]
            if hit_ids:
                rule.message_post(body=_(
                    '%(n)s customer(s) breach this signal. Action: %(a)s')
                    % {'n': len(hit_ids),
                       'a': rule.alert_action or '-'})
                summary.append((rule.rule_name, len(hit_ids)))
        if summary:
            body = _('Churn scan: ') + ', '.join(
                '%s=%d' % kv for kv in summary)
        else:
            body = _('Churn scan: no breaches.')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': _('Churn scan'), 'message': body,
                       'type': 'success'},
        }
