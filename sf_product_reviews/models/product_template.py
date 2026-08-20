# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sf_product_review_ids = fields.One2many('sf.product.review', 'product_id',
                                            string='Product Reviews')
    sf_review_avg = fields.Float(string='Average Rating',
                                 compute='_compute_sf_reviews', store=True)
    sf_review_count = fields.Integer(string='Review Count',
                                     compute='_compute_sf_reviews', store=True)

    @api.depends('sf_product_review_ids.state')
    def _compute_sf_reviews(self):
        for product in self:
            reviews = product.sf_product_review_ids.filtered(
                lambda review: review.state == 'approved'
                and (review.company_id.id == product.company_id.id or not product.company_id))
            product.sf_review_count = len(reviews)
            product.sf_review_avg = reviews and round(
                sum(reviews.mapped('rating')) / len(reviews), 1) or 0.0