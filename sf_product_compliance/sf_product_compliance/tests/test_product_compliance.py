# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductCompliance(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Regulation = self.env['sf.product.regulation']
        self.Requirement = self.env['sf.product.compliance.requirement']
        self.Dossier = self.env['sf.product.compliance.dossier']
        self.Certificate = self.env['sf.product.compliance.certificate']
        self.Product = self.env['product.product']
        self.manager_group = self.env.ref(
            'sf_product_compliance.group_compliance_manager')
        self.user_group = self.env.ref(
            'sf_product_compliance.group_compliance_user')

    def _create_product(self, name='Compliant Widget'):
        return self.Product.create({'name': name})

    def _create_regulation(self, code='CE', market='European Union'):
        return self.Regulation.create({'code': code, 'market': market})

    def _create_requirement(self, product, regulation, state='pending'):
        return self.Requirement.create({
            'product_id': product.id,
            'regulation_id': regulation.id,
            'requirement': 'Must comply with the directive.',
            'state': state,
        })

    def _create_dossier(self, product, regulation):
        return self.Dossier.create({
            'product_id': product.id,
            'regulation_id': regulation.id,
        })

    def _create_user(self, name='Compliance User', login='compliance_user',
                     group=None):
        return self.env['res.users'].create({
            'name': name,
            'login': login,
            'groups_id': [(4, (group or self.user_group).id)],
        })

    def test_create_records_with_sequences(self):
        regulation = self._create_regulation()
        product = self._create_product()
        requirement = self._create_requirement(product, regulation)
        dossier = self._create_dossier(product, regulation)
        certificate = self.Certificate.create({
            'product_id': product.id,
            'certificate_number': 'CER-XYZ-1',
            'expiry_date': fields.Date.today() + timedelta(days=90),
        })
        self.assertTrue(regulation.name.startswith('REG-'))
        self.assertTrue(requirement.name.startswith('REQ-'))
        self.assertTrue(dossier.name.startswith('DOS-'))
        self.assertTrue(certificate.name.startswith('CER-'))

    def test_dossier_cannot_be_compliant_with_unsatisfied_requirement(self):
        product = self._create_product()
        regulation = self._create_regulation()
        self._create_requirement(product, regulation, state='pending')
        dossier = self._create_dossier(product, regulation)
        dossier.action_validate()
        with self.assertRaises(UserError):
            dossier.action_mark_compliant()

    def test_dossier_compliant_when_requirements_satisfied(self):
        product = self._create_product()
        regulation = self._create_regulation()
        requirement = self._create_requirement(product, regulation,
                                               state='pending')
        dossier = self._create_dossier(product, regulation)
        dossier.action_validate()
        requirement.action_mark_satisfied()
        dossier.action_mark_compliant()
        self.assertEqual(dossier.state, 'compliant')
        self.assertTrue(dossier.validated_date)
        self.assertTrue(dossier.validated_by)

    def test_expired_certificate_cron(self):
        product = self._create_product()
        certificate = self.Certificate.create({
            'product_id': product.id,
            'certificate_number': 'CER-EXPIRED-1',
            'expiry_date': fields.Date.today() - timedelta(days=5),
        })
        certificate._check_certificate_expiry()
        self.assertEqual(certificate.state, 'expired')
        self.assertTrue(certificate.activity_ids)

    def test_workflow_and_manager_permission(self):
        product = self._create_product()
        regulation = self._create_regulation()
        requirement = self._create_requirement(product, regulation,
                                               state='pending')
        dossier = self._create_dossier(product, regulation)
        user = self._create_user()
        with self.assertRaises(UserError):
            requirement.with_user(user).action_mark_satisfied()
        self.assertEqual(requirement.state, 'pending')
        with self.assertRaises(UserError):
            dossier.with_user(user).action_validate()
        self.assertEqual(dossier.state, 'draft')
        requirement.action_mark_satisfied()
        dossier.action_validate()
        self.assertEqual(dossier.state, 'in_review')
        dossier.action_mark_compliant()
        self.assertEqual(requirement.state, 'satisfied')
        self.assertEqual(dossier.state, 'compliant')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create(
            {'name': 'Compliance Company B'})
        user = self._create_user(name='Compliance Company A User',
                                 login='compliance_company_a_user')
        regulation = self.Regulation.with_company(company_b).create({
            'code': 'UL',
            'market': 'USA',
        })
        self.assertNotIn(regulation, self.Regulation.with_user(user).search(
            [('id', '=', regulation.id)]))

    def test_report_records_exist(self):
        reports = self.env['ir.actions.report'].search([
            ('report_name', 'in', [
                'sf_product_compliance.product_compliance_template',
                'sf_product_compliance.expired_certificates_template',
            ])])
        self.assertEqual(len(reports), 2)