# -*- coding: utf-8 -*-
"""Customer health scoring."""
import dateutil.relativedelta as rd

from odoo import api, fields, models, _


class SfCustomerHealth(models.Model):
    _name = 'sf.customer.health'
    _description = 'Customer Health'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'health_score desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 required=True, tracking=True,
                                 domain=[('customer_rank', '>', 0)])
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    owner_id = fields.Many2one('res.users', string='Account Owner')
    refreshed_at = fields.Datetime(string='Last Refreshed', readonly=True)
    revenue_12m = fields.Float(string='Revenue (12m)', readonly=True)
    revenue_prev_12m = fields.Float(string='Revenue (prev 12m)', readonly=True)
    trend_percent = fields.Float(string='Revenue Trend %', readonly=True)
    last_order_date = fields.Date(string='Last Order', readonly=True)
    days_since_last_order = fields.Integer(string='Days Since Last Order',
                                           readonly=True)
    overdue_amount = fields.Float(string='Overdue Receivable', readonly=True)
    health_score = fields.Float(string='Health Score (0-100)', readonly=True)
    risk = fields.Selection([
        ('healthy', 'Healthy'), ('watch', 'Watch'),
        ('at_risk', 'At Risk'), ('churn', 'Churn Risk')],
        compute='_compute_risk', store=True)
    next_action_date = fields.Date(string='Next Action Date')
    next_action_note = fields.Char(string='Next Action')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer.health') or 'CHL-NEW'
        return super().create(vals_list)

    @api.depends('health_score', 'overdue_amount')
    def _compute_risk(self):
        for rec in self:
            if rec.overdue_amount > 0:
                rec.risk = 'at_risk'
            elif rec.health_score >= 70:
                rec.risk = 'healthy'
            elif rec.health_score >= 45:
                rec.risk = 'watch'
            else:
                rec.risk = 'churn'

    def action_refresh(self):
        today = fields.Date.context_today(self)
        for rec in self:
            start12 = today - rd.relativedelta(months=12)
            start24 = today - rd.relativedelta(months=24)
            inv_domain = [
                ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                ('partner_id', '=', rec.partner_id.id),
                ('company_id', '=', rec.company_id.id)]
            revenue = sum(self.env['account.move'].search(
                inv_domain + [('invoice_date', '>=', start12)]).mapped(
                'amount_untaxed'))
            prev_revenue = sum(self.env['account.move'].search(
                inv_domain + [('invoice_date', '>=', start24),
                              ('invoice_date', '<', start12)]).mapped(
                'amount_untaxed'))
            last_order = self.env['sale.order'].search(
                [('partner_id', '=', rec.partner_id.id),
                 ('state', 'in', ('sale', 'done')),
                 ('company_id', '=', rec.company_id.id)],
                order='date_order desc', limit=1)
            last_date = (last_order.date_order.date()
                         if last_order else start24)
            days_since = (today - last_date).days
            overdue = sum(self.env['account.move.line'].search([
                ('partner_id', '=', rec.partner_id.id),
                ('account_id.account_type', '=', 'asset_receivable'),
                ('reconciled', '=', False),
                ('company_id', '=', rec.company_id.id)]).mapped(
                'amount_residual'))
            trend = ((revenue - prev_revenue) / prev_revenue * 100.0
                     if prev_revenue else (100.0 if revenue else 0.0))
            # Score: recency (40) + trend (35) + no-overdue (25)
            recency_score = max(0.0, 40.0 - days_since * 0.15)
            trend_score = max(0.0, min(35.0, 17.5 + trend * 0.35))
            overdue_score = 25.0 if overdue <= 0 else max(
                0.0, 25.0 - overdue / 100.0)
            rec.write({
                'revenue_12m': revenue,
                'revenue_prev_12m': prev_revenue,
                'trend_percent': trend,
                'last_order_date': last_date,
                'days_since_last_order': days_since,
                'overdue_amount': overdue,
                'health_score': round(recency_score + trend_score
                                      + overdue_score, 1),
                'refreshed_at': fields.Datetime.now()})


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.customer.health'

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
