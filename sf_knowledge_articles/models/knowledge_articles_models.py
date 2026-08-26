# -*- coding: utf-8 -*-
"""Knowledge Article Library models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfKnowledgeArticle(models.Model):
    _name = 'sf.knowledge.article'
    _description = 'Knowledge Article'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Title', required=True)
    category = fields.Selection([
        ('howto', 'How-To'),
        ('troubleshooting', 'Troubleshooting'),
        ('policy', 'Policy'),
        ('reference', 'Reference'),
        ], string='Category', required=True, default=howto)
    content = fields.Html(string='Content')
    author_id = fields.Many2one('res.users', string='Author')
    review_date = fields.Date(string='Next Review')
    views = fields.Integer(string='Views')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('published', 'Published'),
        ('needs_update', 'Needs Update'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.knowledge.article') or 'NEW'
        return super().create(vals_list)

    def action_review(self):
        self.write({'state': 'review'})

    def action_published(self):
        self.write({'state': 'published'})

    def action_needs_update(self):
        self.write({'state': 'needs_update'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.knowledge.article'

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

