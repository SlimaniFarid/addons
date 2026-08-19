# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo.tests import TransactionalCase, tagged


@tagged('post_install', '-at_install')
class TestProductPim(TransactionalCase):

    def setUp(self):
        super().setUp()
        self.Product = self.env['product.template']
        self.Category = self.env['sf.pim.category']
        self.Attribute = self.env['sf.pim.attribute']
        self.Channel = self.env['sf.pim.channel']
        self.Publication = self.env['sf.pim.publication']
        self.Review = self.env['sf.pim.review']
        self.env.user.groups_id += self.env.ref(
            'sf_product_pim.group_pim_manager')

    def _create_family(self):
        category = self.Category.create({'name': 'Test Family'})
        self.Attribute.create({
            'name': 'Material', 'category_id': category.id,
            'field_type': 'text', 'required': True,
        })
        self.Attribute.create({
            'name': 'Weight', 'category_id': category.id,
            'field_type': 'numeric', 'required': True,
        })
        self.Attribute.create({
            'name': 'Certification', 'category_id': category.id,
            'field_type': 'selection', 'required': True,
        })
        return category

    def _create_channel(self):
        return self.Channel.create({'name': 'Webshop'})

    def test_create_family_and_score(self):
        category = self._create_family()
        product = self.Product.create({
            'name': 'Widget',
            'pim_category_id': category.id,
        })
        self.assertEqual(product.pim_score, 0.0)
        product.write({
            'pim_attributes': [
                (0, 0, {'attribute_id': category.attribute_ids[0].id,
                        'value': 'Steel'}),
            ],
        })
        self.assertAlmostEqual(product.pim_score, 33.33, places=1)
        product.pim_attributes[0].value = 'Steel'
        for attr in category.attribute_ids:
            self.env['sf.pim.product.attribute'].create({
                'product_tmpl_id': product.id,
                'attribute_id': attr.id,
                'value': 'X',
            })
        self.assertEqual(product.pim_score, 100.0)

    def test_score_without_family(self):
        product = self.Product.create({'name': 'Bare'})
        self.assertGreater(product.pim_score, 0.0)

    def test_workflow_approve(self):
        product = self.Product.create({'name': 'Workflow'})
        self.assertEqual(product.pim_state, 'draft')
        product.action_submit()
        self.assertEqual(product.pim_state, 'in_review')
        product.action_approve()
        self.assertEqual(product.pim_state, 'approved')

    def test_reject_returns_draft(self):
        product = self.Product.create({'name': 'Reject'})
        product.action_submit()
        wizard = self.env['sf.pim.reject.wizard'].create({
            'product_tmpl_id': product.id,
            'reason': 'Missing certification',
        })
        wizard.action_reject()
        self.assertEqual(product.pim_state, 'draft')

    def test_publish_requires_approved(self):
        product = self.Product.create({'name': 'Publish'})
        with self.assertRaises(UserError):
            product.action_publish()

    def test_publish_and_withdraw(self):
        category = self._create_family()
        product = self.Product.create({'name': 'Publishable',
                                       'pim_category_id': category.id})
        for attr in category.attribute_ids:
            self.env['sf.pim.product.attribute'].create({
                'product_tmpl_id': product.id,
                'attribute_id': attr.id,
                'value': 'OK',
            })
        channel = self._create_channel()
        product.action_submit()
        product.action_approve()
        product.action_publish()
        wizard = self.env['sf.pim.publish.wizard'].with_context(
            active_id=product.id).create({
                'product_tmpl_id': product.id,
                'channel_id': channel.id,
            })
        wizard.action_publish()
        self.assertEqual(product.pim_state, 'published')
        self.assertIn(channel, product.pim_channel_ids)
        product.action_withdraw()
        self.assertNotIn(channel, product.pim_channel_ids)

    def test_unique_publication_constraint(self):
        category = self._create_family()
        product = self.Product.create({'name': 'Dup',
                                       'pim_category_id': category.id})
        for attr in category.attribute_ids:
            self.env['sf.pim.product.attribute'].create({
                'product_tmpl_id': product.id,
                'attribute_id': attr.id,
                'value': 'OK',
            })
        channel = self._create_channel()
        self.Publication.create({
            'product_tmpl_id': product.id,
            'channel_id': channel.id,
        })
        with self.assertRaises(Exception):
            self.Publication.create({
                'product_tmpl_id': product.id,
                'channel_id': channel.id,
            })

    def test_required_attribute_cleared_returns_draft(self):
        category = self._create_family()
        product = self.Product.create({'name': 'Consistency',
                                       'pim_category_id': category.id})
        for attr in category.attribute_ids:
            self.env['sf.pim.product.attribute'].create({
                'product_tmpl_id': product.id,
                'attribute_id': attr.id,
                'value': 'OK',
            })
        channel = self._create_channel()
        product.action_submit()
        product.action_approve()
        self.Publication.create({
            'product_tmpl_id': product.id,
            'channel_id': channel.id,
        })
        product.pim_state = 'published'
        product.pim_attributes[0].value = False
        self.assertEqual(product.pim_state, 'draft')

    def test_approval_reserved_for_manager(self):
        user = self.env['res.users'].create({
            'name': 'PIM Plain User',
            'login': 'pim_plain_user',
            'groups_id': [(4, self.env.ref('sf_product_pim.group_pim_user').id)],
        })
        product = self.Product.create({'name': 'Secure'})
        product.action_submit()
        with self.assertRaises(AccessError):
            product.with_user(user).action_approve()

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Company B'})
        user = self.env['res.users'].create({
            'name': 'PIM Company A User',
            'login': 'pim_company_a_user',
            'groups_id': [(4, self.env.ref('sf_product_pim.group_pim_user').id)],
        })
        other = self.Category.with_company(company_b).create(
            {'name': 'Other Company Family'})
        self.assertNotIn(other, self.Category.with_user(user).search(
            [('id', '=', other.id)]))