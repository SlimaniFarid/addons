# -*- coding: utf-8 -*-
"""Supplier Scorecard Review Meetings models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierReview(models.Model):
    _name = 'sf.supplier.review'
    _description = 'Supplier Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    review_date = fields.Date(string='Review Date', required=True, default=fields.Date.today)
    quality_score = fields.Float(string='Quality Score')
    delivery_score = fields.Float(string='Delivery Score')
    actions = fields.Html(string='Improvement Actions')
    next_review = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('held', 'Held'),
        ('actions_tracked', 'Actions Tracked'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.review') or 'NEW'
        return super().create(vals_list)

    def action_held(self):
        self.write({'state': 'held'})

    def action_actions_tracked(self):
        self.write({'state': 'actions_tracked'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.supplier.review'

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


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.supplier.review'

    def action_refresh_business(self):
        """Pull PO count and total for linked vendor."""
        for rec in self:
            vendor = getattr(rec, 'vendor_id',
                             getattr(rec, 'partner_id', False))
            if not vendor:
                continue
            pos = self.env['purchase.order'].search([
                ('partner_id', '=', vendor.id),
                ('state', 'in', ('purchase', 'done'))])
            rec.message_post(body=_(
                '{n} confirmed PO(s), total {t:.2f}.').format(
                n=len(pos), t=sum(pos.mapped('amount_total'))))
        return True
