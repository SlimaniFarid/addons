# -*- coding: utf-8 -*-
import uuid

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfProductReviews(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.product = self.env['product.template'].create({
            'name': 'Reviewed Product %s' % uuid.uuid4().hex[:4],
            'type': 'service',
        })
        self.pricelist = self.env['product.pricelist'].create({
            'name': 'Test Pricelist %s' % uuid.uuid4().hex[:4],
            'currency_id': self.env.company.currency_id.id,
        })

    def _create_review(self, rating=5, **kw):
        vals = {
            'product_id': self.product.id,
            'partner_id': self.customer.id,
            'author_name': 'Claire',
            'rating': rating,
            'title': 'Great product',
            'body': 'Very happy with this purchase.',
        }
        vals.update(kw)
        return self.env['sf.product.review'].create(vals)

    def test_sequence(self):
        review = self._create_review()
        self.assertTrue(review.name.startswith('RVR-'))

    def test_rating_constraint(self):
        with self.assertRaises(ValidationError):
            self._create_review(rating=0)
        with self.assertRaises(ValidationError):
            self._create_review(rating=6)

    def test_workflow_approve(self):
        review = self._create_review()
        self.assertEqual(review.state, 'draft')
        review.action_submit()
        self.assertEqual(review.state, 'submitted')
        review.action_approve()
        self.assertEqual(review.state, 'approved')

    def test_workflow_reject(self):
        review = self._create_review()
        review.action_submit()
        review.action_reject()
        self.assertEqual(review.state, 'rejected')

    def test_submit_requires_draft(self):
        review = self._create_review()
        review.action_submit()
        with self.assertRaises(UserError):
            review.action_submit()

    def test_approve_requires_submitted(self):
        review = self._create_review()
        with self.assertRaises(UserError):
            review.action_approve()

    def test_archive_approved(self):
        review = self._create_review()
        review.action_submit()
        review.action_approve()
        review.action_archive()
        self.assertEqual(review.state, 'archived')

    def test_archive_requires_approved(self):
        review = self._create_review()
        with self.assertRaises(UserError):
            review.action_archive()

    def test_aggregation_approved_only(self):
        r1 = self._create_review(rating=4)
        r1.action_submit()
        r1.action_approve()
        r2 = self._create_review(rating=5)
        r2.action_submit()
        r2.action_approve()
        r3 = self._create_review(rating=1)
        r3.action_submit()
        r3.action_reject()
        self.assertEqual(self.product.sf_review_count, 2)
        self.assertEqual(self.product.sf_review_avg, 4.5)

    def test_aggregation_excludes_archived(self):
        r1 = self._create_review(rating=5)
        r1.action_submit()
        r1.action_approve()
        r2 = self._create_review(rating=1)
        r2.action_submit()
        r2.action_approve()
        r2.action_archive()
        self.assertEqual(self.product.sf_review_count, 1)
        self.assertEqual(self.product.sf_review_avg, 5.0)

    def test_no_aggregation_before_approval(self):
        review = self._create_review(rating=5)
        review.action_submit()
        self.assertEqual(self.product.sf_review_count, 0)
        review.action_approve()
        self.assertEqual(self.product.sf_review_count, 1)

    def test_verified_purchase(self):
        order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [(0, 0, {
                'product_id': self.product.product_variant_id.id,
                'product_uom_qty': 1,
            })],
        })
        order.action_confirm()
        review = self._create_review()
        self.assertTrue(review.verified_purchase)

    def test_not_verified_purchase(self):
        review = self._create_review()
        self.assertFalse(review.verified_purchase)

    def test_auto_approve_without_moderation(self):
        self.env['ir.config_parameter'].set_param(
            'sf_product_reviews.moderation_required', 'False')
        self.env['ir.config_parameter'].set_param(
            'sf_product_reviews.approval_threshold', '4')
        review = self._create_review(rating=5)
        review.action_submit()
        self.assertEqual(review.state, 'approved')
        low = self._create_review(rating=2)
        low.action_submit()
        self.assertEqual(low.state, 'submitted')

    def test_permissions(self):
        user = self.env['res.users'].create({
            'name': 'Review User %s' % uuid.uuid4().hex[:4],
            'login': 'rv_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_product_reviews.group_sf_product_reviews_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        review = self._create_review()
        review.action_submit()
        with self.assertRaises(UserError):
            review.with_user(user).action_approve()
        with self.assertRaises(UserError):
            review.with_user(user).action_reject()

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Reviews Co 2'})
        product2 = self.env['product.template'].with_company(company2).create({
            'name': 'Product Company 2',
            'type': 'service',
            'company_id': company2.id,
        })
        review2 = self.env['sf.product.review'].with_company(company2).create({
            'product_id': product2.id,
            'partner_id': self.customer.id,
            'author_name': 'Tom',
            'rating': 5,
            'company_id': company2.id,
        })
        self.assertEqual(review2.company_id, company2)
        user = self.env['res.users'].create({
            'name': 'Review User %s' % uuid.uuid4().hex[:4],
            'login': 'rv_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_product_reviews.group_sf_product_reviews_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.product.review'].with_user(user).search([('id', '=', review2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        review = self._create_review(rating=4)
        review.action_submit()
        review.action_approve()
        action = self.env.ref(
            'sf_product_reviews.action_report_product_review').report_action(review)
        self.assertTrue(action)