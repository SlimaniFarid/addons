# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfProductReview(models.Model):
    _name = 'sf.product.review'
    _description = 'Product Review'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.product.reviews.activity.mixin']
    _order = 'review_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    product_id = fields.Many2one('product.template', string='Product', required=True,
                                 ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='set null')
    author_name = fields.Char(string='Author Name')
    rating = fields.Integer(string='Rating', required=True)
    title = fields.Char(string='Title')
    body = fields.Text(string='Comment')
    verified_purchase = fields.Boolean(string='Verified Purchase',
                                       compute='_compute_verified_purchase', store=True)
    reply = fields.Text(string='Reply')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', copy=False)
    review_date = fields.Date(string='Review Date', default=lambda self: fields.Date.context_today(self))
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('rating_range', 'CHECK (rating >= 1 AND rating <= 5)',
         'The rating must be between 1 and 5.'),
    ]

    @api.depends('partner_id', 'product_id', 'company_id')
    def _compute_verified_purchase(self):
        # sudo() is required because sale.order.line access is restricted by company
        # and the review's company_id may differ from the user's current company.
        # The search is limited to the review's own company_id for security.
        for review in self:
            verified = False
            if review.partner_id:
                line = self.env['sale.order.line'].sudo().search([
                    ('order_partner_id', '=', review.partner_id.id),
                    ('order_id.state', '=', 'sale'),
                    ('product_id.product_tmpl_id', '=', review.product_id.id),
                    ('order_id.company_id', '=', review.company_id.id),
                ], limit=1)
                verified = bool(line)
            review.verified_purchase = verified

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.product.review')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_product_reviews.group_sf_product_reviews_manager'):
            raise UserError(_('Only a product reviews manager can perform this action.'))

    def action_submit(self):
        for review in self:
            if review.state != 'draft':
                raise UserError(_('Only draft reviews can be submitted.'))
            moderation_required = self.env['ir.config_parameter'].sudo().get_param(
                'sf_product_reviews.moderation_required', 'True') == 'True'
            threshold = int(self.env['ir.config_parameter'].sudo().get_param(
                'sf_product_reviews.approval_threshold', '4'))
            if not moderation_required and review.rating >= threshold:
                review.state = 'approved'
                review.message_post(body=_('The review was automatically approved.'))
            else:
                review.state = 'submitted'
                review.message_post(body=_('The review was submitted for moderation.'))

    def action_approve(self):
        self._check_manager()
        for review in self:
            if review.state != 'submitted':
                raise UserError(_('Only submitted reviews can be approved.'))
            review.state = 'approved'
            review.message_post(body=_('The review was approved.'))

    def action_reject(self):
        self._check_manager()
        for review in self:
            if review.state != 'submitted':
                raise UserError(_('Only submitted reviews can be rejected.'))
            review.state = 'rejected'
            review.message_post(body=_('The review was rejected.'))

    def action_archive(self):
        self._check_manager()
        for review in self:
            if review.state != 'approved':
                raise UserError(_('Only approved reviews can be archived.'))
            review.state = 'archived'
            review.message_post(body=_('The review was archived.'))