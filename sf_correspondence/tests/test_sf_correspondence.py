# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfCorrespondence(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Correspondent %s' % uuid.uuid4().hex[:6],
        })
        self.department = self.env['sf.correspondence.department'].create({
            'name': 'Legal',
        })
        self.todo = self.env.ref('mail.mail_activity_data_todo')

    def _create_correspondence(self, **kw):
        vals = {
            'direction': 'inbound',
            'partner_id': self.partner.id,
            'subject': 'Complaint',
        }
        vals.update(kw)
        return self.env['sf.correspondence'].create(vals)

    def test_sequences(self):
        record = self._create_correspondence()
        self.assertTrue(record.name.startswith('COR-'))
        department = self.env['sf.correspondence.department'].create({})
        self.assertTrue(department.name.startswith('DEP-'))

    def test_workflow(self):
        record = self._create_correspondence()
        record.action_open()
        self.assertEqual(record.state, 'open')
        record.action_start()
        self.assertEqual(record.state, 'in_progress')
        record.action_responded()
        self.assertEqual(record.state, 'responded')
        self.assertTrue(record.response_date)
        record.action_archive()
        self.assertEqual(record.state, 'archived')

    def test_state_write_guard(self):
        record = self._create_correspondence()
        with self.assertRaises(UserError):
            record.write({'state': 'open'})

    def test_responded_requires_prior_state(self):
        record = self._create_correspondence()
        with self.assertRaises(UserError):
            record.action_responded()

    def test_cancel_requires_manager(self):
        user = self.env['res.users'].create({
            'name': 'Corr User',
            'login': 'corr_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_correspondence.group_sf_correspondence_user').id])],
        })
        record = self._create_correspondence().with_user(user)
        record.action_open()
        with self.assertRaises(UserError):
            record.action_cancel()

    def test_cancel_archived_blocked(self):
        record = self._create_correspondence()
        record.action_open()
        record.action_responded()
        record.action_archive()
        with self.assertRaises(UserError):
            record.action_cancel()

    def test_cron_followups(self):
        today = odoo_fields.Date.today()
        due = self._create_correspondence(
            response_due_date=today - timedelta(days=1))
        due.action_open()
        ok = self._create_correspondence(
            response_due_date=today - timedelta(days=1))
        ok.action_open()
        ok.action_responded()
        self.env['sf.correspondence']._cron_followups()
        self.assertTrue(due.activity_ids)
        self.assertFalse(ok.activity_ids)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({
            'name': 'Correspondence Co 2'})
        record2 = self.env['sf.correspondence'].with_company(company2).create({
            'direction': 'outbound',
            'partner_id': self.partner.id,
            'subject': 'Notice',
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'Corr User 2',
            'login': 'corr_user2_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_correspondence.group_sf_correspondence_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.correspondence'].with_user(user).search(
            [('id', '=', record2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        record = self._create_correspondence()
        for report in ['action_report_correspondence_register',
                       'action_report_correspondence_sheet']:
            action = self.env.ref(
                'sf_correspondence.%s' % report).report_action(record)
            self.assertTrue(action)