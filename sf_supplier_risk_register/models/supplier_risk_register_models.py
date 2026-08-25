# -*- coding: utf-8 -*-
"""Supplier Risk Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierRisk(models.Model):
    _name = 'sf.supplier.risk'
    _description = 'Supplier Risk'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    risk_type = fields.Selection([
        ('financial', 'Financial'),
        ('geo', 'Geographic'),
        ('single_source', 'Single Source'),
        ('compliance', 'Compliance'),
        ('capacity', 'Capacity'),
        ], string='Risk Type', required=True)
    score = fields.Integer(string='Risk Score (1-25)')
    mitigation = fields.Text(string='Mitigation Plan')
    contingency = fields.Text(string='Contingency (Backup Source)')
    review_date = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('identified', 'Identified'),
        ('mitigating', 'Mitigating'),
        ('closed', 'Closed'),
        ], string='Status', default='identified', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.risk') or 'NEW'
        return super().create(vals_list)

    def action_mitigating(self):
        self.write({'state': 'mitigating'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.supplier.risk'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('review_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.review_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

