# -*- coding: utf-8 -*-
"""Decision Log with Context models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDecision(models.Model):
    _name = 'sf.decision'
    _description = 'Decision Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Decision Title', required=True)
    date = fields.Date(string='Decision Date', required=True, default=fields.Date.today)
    context = fields.Html(string='Context & Options')
    rationale = fields.Text(string='Rationale')
    decision_maker_id = fields.Many2one('res.users', string='Decision Maker')
    review_date = fields.Date(string='Review If Still Valid')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('recorded', 'Recorded'),
        ('superseded', 'Superseded'),
        ], string='Status', default='recorded', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.decision') or 'NEW'
        return super().create(vals_list)

    def action_superseded(self):
        self.write({'state': 'superseded'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.decision'

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

