# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields


class TestCompliance(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Doc = self.env['sf.compliance.document']
        self.Type = self.env['sf.compliance.document.type']
        self.History = self.env['sf.compliance.history']
        self.responsible = self.env['res.users'].create({
            'name': 'Responsible',
            'login': 'compliance_resp_test',
        })
        self.manager = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'compliance_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref(
                        'sf_compliance_register.group_compliance_manager').id,
                ]),
            ],
        })
        self.user = self.env['res.users'].create({
            'name': 'User',
            'login': 'compliance_user_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref(
                        'sf_compliance_register.group_compliance_user').id,
                ]),
            ],
        })
        self.doc_type = self.Type.create({
            'name': 'Insurance',
            'code': 'INS',
            'category': 'insurance',
            'default_alert_days': 30,
        })

    def _make_doc(self, **kw):
        today = fields.Date.today()
        vals = {
            'name': 'Public liability insurance',
            'document_type_id': self.doc_type.id,
            'issue_date': today,
            'expiry_date': fields.Date.from_string('2027-12-31'),
            'responsible_id': self.responsible.id,
        }
        vals.update(kw)
        return self.Doc.create(vals)

    def test_01_publish_workflow(self):
        doc = self._make_doc()
        self.assertEqual(doc.state, 'draft')
        doc.action_publish()
        self.assertEqual(doc.state, 'active')
        self.assertEqual(doc.published, True)

    def test_02_expiring_state(self):
        today = fields.Date.today()
        doc = self._make_doc(
            issue_date=fields.Date.from_string('2025-01-01'),
            expiry_date=today + fields.timedelta(days=10))
        doc.action_publish()
        self.assertEqual(doc.state, 'expiring')

    def test_03_expired_state(self):
        doc = self._make_doc(
            issue_date=fields.Date.from_string('2024-01-01'),
            expiry_date=fields.Date.from_string('2025-01-01'))
        doc.action_publish()
        self.assertEqual(doc.state, 'expired')

    def test_04_renewal_creates_new_document(self):
        doc = self._make_doc(
            issue_date=fields.Date.from_string('2025-01-01'),
            expiry_date=fields.Date.from_string('2026-01-01'))
        doc.action_publish()
        wizard = self.env['sf.compliance.renew.wizard'].create({
            'document_id': doc.id,
            'new_expiry_date': fields.Date.from_string('2028-06-30'),
        })
        wizard.action_renew()
        renewed = doc.renewed_by_id
        self.assertTrue(renewed)
        self.assertEqual(renewed.state, 'active')
        self.assertEqual(renewed.expiry_date,
                         fields.Date.from_string('2028-06-30'))
        history = self.History.search([
            ('document_id', '=', renewed.id),
            ('action', '=', 'renewed'),
        ])
        self.assertEqual(len(history), 1)
        self.assertFalse(doc.active)

    def test_05_renewal_past_date_rejected(self):
        doc = self._make_doc()
        doc.action_publish()
        wizard = self.env['sf.compliance.renew.wizard'].create({
            'document_id': doc.id,
            'new_expiry_date': fields.Date.from_string('2020-01-01'),
        })
        with self.assertRaises(UserError):
            wizard.action_renew()

    def test_06_attachment_required(self):
        self.env.company.sf_compliance_require_attachment = True
        doc = self._make_doc()
        with self.assertRaises(UserError):
            doc.action_publish()

    def test_07_bad_dates_rejected(self):
        with self.assertRaises(UserError):
            self._make_doc(
                issue_date=fields.Date.from_string('2026-12-31'),
                expiry_date=fields.Date.from_string('2026-01-01'))

    def test_08_published_not_deletable(self):
        doc = self._make_doc()
        doc.action_publish()
        with self.assertRaises(UserError):
            doc.unlink()

    def test_09_alert_creates_activity(self):
        today = fields.Date.today()
        doc = self._make_doc(
            issue_date=fields.Date.from_string('2025-01-01'),
            expiry_date=today + fields.timedelta(days=10))
        doc.action_publish()
        self.assertEqual(doc.state, 'expiring')
        doc._check_expiry_alerts()
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'sf.compliance.document'),
            ('res_id', '=', doc.id),
        ])
        self.assertTrue(activities)

    def test_10_default_alert_days(self):
        doc = self._make_doc()
        self.assertEqual(doc.alert_days, 30)