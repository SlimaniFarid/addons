# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestCorporateSecretary(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Org = self.env['sf.corporate.org']
        self.Meeting = self.env['sf.corporate.meeting']
        self.Resolution = self.env['sf.corporate.resolution']
        self.Decision = self.env['sf.corporate.legal.decision']
        self.Formality = self.env['sf.corporate.formality']
        self.group_user = self.env.ref(
            'sf_corporate_secretary.group_corporate_user')
        self.group_manager = self.env.ref(
            'sf_corporate_secretary.group_corporate_manager')

    def _create_org(self, notice_days=15):
        partner = self.env['res.partner'].create({'name': 'Chair Partner'})
        return self.Org.create({
            'org_type': 'aga',
            'notice_days': notice_days,
            'chairperson_id': partner.id,
            'members': [(6, 0, [partner.id])],
        })

    def _create_meeting(self, scheduled_date=None):
        org = self._create_org()
        return self.Meeting.create({
            'org_id': org.id,
            'scheduled_date': scheduled_date or fields.Date.today(),
            'location': 'Head Office',
        })

    def test_create_records_with_sequences(self):
        org = self._create_org()
        meeting = self._create_meeting()
        resolution = self.Resolution.create({
            'meeting_id': meeting.id,
            'number': 1,
            'subject': 'Approve annual accounts',
            'vote_for': 5,
            'vote_against': 1,
        })
        decision = self.Decision.create({
            'title': 'Approve bank loan',
            'decision_date': fields.Date.today(),
        })
        formality = self.Formality.create({
            'formality_type': 'financial_filing',
            'due_date': fields.Date.today() + timedelta(days=30),
        })
        self.assertTrue(org.name.startswith('ORG-'))
        self.assertTrue(meeting.name.startswith('MEE-'))
        self.assertTrue(resolution.name.startswith('RES-'))
        self.assertTrue(decision.name.startswith('DEC-'))
        self.assertTrue(formality.name.startswith('FOR-'))

    def test_notice_date_computed(self):
        scheduled = fields.Date.today() + timedelta(days=30)
        meeting = self._create_meeting(scheduled_date=scheduled)
        self.assertEqual(meeting.notice_date, scheduled - timedelta(days=15))
        self.env.company.sf_corporate_default_notice_days = 20
        org = self._create_org(notice_days=0)
        meeting2 = self.Meeting.create({
            'org_id': org.id,
            'scheduled_date': scheduled,
        })
        self.assertEqual(meeting2.notice_date, scheduled - timedelta(days=20))

    def test_resolution_adopted_rule(self):
        meeting = self._create_meeting()
        resolution = self.Resolution.create({
            'meeting_id': meeting.id,
            'number': 1,
            'subject': 'Approve annual accounts',
            'vote_for': 5,
            'vote_against': 5,
        })
        self.assertFalse(resolution.adopted)
        resolution.write({'vote_for': 6})
        self.assertTrue(resolution.adopted)
        resolution.write({'vote_against': 6})
        self.assertFalse(resolution.adopted)

    def test_meeting_done_requires_minutes(self):
        meeting = self._create_meeting()
        meeting.action_start_meeting()
        with self.assertRaises(UserError):
            meeting.action_done()

    def test_meeting_done_manager_only(self):
        meeting = self._create_meeting()
        meeting.action_start_meeting()
        meeting.minutes = '<p>Minutes of the meeting</p>'
        user = self.env['res.users'].create({
            'name': 'Corporate User',
            'login': 'corporate_user',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_user.id)],
        })
        with self.assertRaises(UserError):
            meeting.with_user(user).action_done()

    def test_meeting_done_as_manager(self):
        meeting = self._create_meeting()
        meeting.action_start_meeting()
        meeting.minutes = '<p>Minutes of the meeting</p>'
        manager = self.env['res.users'].create({
            'name': 'Corporate Manager',
            'login': 'corporate_manager',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_user.id),
                          (4, self.group_manager.id)],
        })
        meeting.with_user(manager).action_done()
        self.assertEqual(meeting.state, 'done')
        self.assertTrue(meeting.minutes_done_date)
        self.assertTrue(meeting.recorded_by)

    def test_convocation_workflow(self):
        meeting = self._create_meeting()
        self.assertEqual(meeting.convocation_state, 'draft')
        meeting.action_convocation_sent()
        self.assertEqual(meeting.convocation_state, 'sent')
        self.assertTrue(meeting.notice_sent)
        meeting.action_convocation_held()
        self.assertEqual(meeting.convocation_state, 'held')
        meeting.minutes = '<p>Minutes</p>'
        meeting.action_convocation_pv_done()
        self.assertEqual(meeting.convocation_state, 'pv_done')

    def test_cron_check_formalities(self):
        today = fields.Date.today()
        formality = self.Formality.create({
            'formality_type': 'statutory',
            'due_date': today,
            'reminder_days': 30,
        })
        meeting = self._create_meeting(scheduled_date=today)
        self.Formality._check_formalities()
        self.assertTrue(formality.activity_ids)
        self.assertTrue(meeting.activity_ids)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Corp Company B'})
        user = self.env['res.users'].create({
            'name': 'Corp Company A User',
            'login': 'corp_company_a_user',
            'company_id': self.env.company.id,
            'company_ids': [(6, 0, [self.env.company.id])],
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Formality.with_company(company_b).create({
            'formality_type': 'other',
            'due_date': fields.Date.today(),
        })
        self.assertNotIn(other, self.Formality.with_user(user).search(
            [('id', '=', other.id)]))

    def test_reports_exist(self):
        minutes_report = self.env.ref(
            'sf_corporate_secretary.report_meeting_minutes')
        schedule_report = self.env.ref(
            'sf_corporate_secretary.report_formality_schedule')
        self.assertTrue(minutes_report)
        self.assertTrue(schedule_report)
        self.assertEqual(minutes_report.model, 'sf.corporate.meeting')
        self.assertEqual(schedule_report.model, 'sf.corporate.formality')