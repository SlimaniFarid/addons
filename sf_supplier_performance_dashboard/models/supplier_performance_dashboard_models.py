# -*- coding: utf-8 -*-
"""Supplier Performance Dashboard Config models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_performance_dashboard(models.Model):
    _name = 'sf.supplier_performance_dashboard'
    _description = 'Supplier Performance Dashboard Config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    metric_name = fields.Char(string='Metric', required=True)
    metric_type = fields.Selection([
        ('otd', 'On-Time Delivery'),
        ('quality', 'Quality'),
        ('price', 'Price Competitiveness'),
        ('responsiveness', 'Responsiveness'),
        ], string='Type', required=True)
    target = fields.Float(string='Target')
    alert_threshold = fields.Float(string='Alert Threshold')
    review_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ], string='Frequency', default=quarterly)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier_performance_dashboard') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_review(self):
        self.write({'state': 'review'})

    def action_done(self):
        self.write({'state': 'done'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.supplier_performance_dashboard'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

