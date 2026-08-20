# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfGymFitness(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Member = self.env['sf.gym.member']
        self.Plan = self.env['sf.gym.plan']
        self.Lesson = self.env['sf.gym.lesson']
        self.Subscription = self.env['sf.gym.subscription']
        self.Session = self.env['sf.gym.session']
        self.Attendance = self.env['sf.gym.attendance']
        self.Payment = self.env['sf.gym.payment']
        self.group_user = self.env.ref('sf_gym_fitness.group_sf_gym_user')
        self.group_manager = self.env.ref('sf_gym_fitness.group_sf_gym_manager')
        self.user = self.env['res.users'].create({
            'name': 'Gym User',
            'login': 'gym_user',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Gym Manager',
            'login': 'gym_manager',
            'groups_id': [(4, self.group_manager.id)],
        })
        self.plain_user = self.env['res.users'].create({
            'name': 'Plain User',
            'login': 'plain_user',
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        })

    def _create_member(self, name='John Doe'):
        partner = self.env['res.partner'].create({'name': name})
        return self.Member.create({
            'partner_id': partner.id,
            'phone': '0123456789',
            'email': 'john@example.com',
        })

    def _create_plan(self, price=50.0, months=3):
        return self.Plan.create({
            'code': 'STD',
            'price_monthly': price,
            'duration_months': months,
        })

    def _create_lesson(self, capacity=5):
        return self.Lesson.create({'capacity': capacity})

    def _create_subscription(self, member=None, plan=None):
        return self.Subscription.create({
            'member_id': (member or self._create_member()).id,
            'plan_id': (plan or self._create_plan()).id,
            'start_date': fields.Date.today(),
        })

    def _create_session(self, lesson=None):
        return self.Session.create({
            'lesson_id': (lesson or self._create_lesson()).id,
            'date': fields.Date.today(),
        })

    def test_create_records_with_sequences(self):
        member = self._create_member()
        self.assertTrue(member.name.startswith('MEM-'))
        plan = self._create_plan()
        self.assertTrue(plan.name.startswith('PLA-'))
        lesson = self._create_lesson()
        self.assertTrue(lesson.name.startswith('LES-'))
        subscription = self._create_subscription(member=member, plan=plan)
        self.assertTrue(subscription.name.startswith('SUB-'))
        session = self._create_session(lesson=lesson)
        self.assertTrue(session.name.startswith('SES-'))
        session.action_confirm()
        attendance = self.Attendance.create({
            'session_id': session.id,
            'member_id': member.id,
        })
        self.assertTrue(attendance.name.startswith('ATT-'))
        payment = self.Payment.create({
            'subscription_id': subscription.id,
            'amount': 150.0,
        })
        self.assertTrue(payment.name.startswith('PAY-'))

    def test_computed_end_date_and_price(self):
        plan = self._create_plan(price=50.0, months=3)
        subscription = self._create_subscription(plan=plan)
        start = subscription.start_date
        expected_end = start.replace(
            year=start.year + (start.month - 1 + 3) // 12,
            month=(start.month - 1 + 3) % 12 + 1)
        self.assertEqual(subscription.end_date, expected_end)
        self.assertEqual(subscription.price, 150.0)

    def test_attendance_count_and_capacity_limit(self):
        lesson = self._create_lesson(capacity=2)
        session = self._create_session(lesson=lesson)
        session.action_confirm()
        member1 = self._create_member('Alice')
        member2 = self._create_member('Bob')
        self.Attendance.create({
            'session_id': session.id,
            'member_id': member1.id,
        })
        self.Attendance.create({
            'session_id': session.id,
            'member_id': member2.id,
        })
        self.assertEqual(session.attendance_count, 2)
        self.assertEqual(session.capacity, 2)
        member3 = self._create_member('Carol')
        with self.assertRaises(UserError):
            self.Attendance.create({
                'session_id': session.id,
                'member_id': member3.id,
            })

    def test_session_status_reserved_to_coach_and_manager(self):
        coach = self.env['res.users'].create({
            'name': 'Coach',
            'login': 'coach',
            'groups_id': [(4, self.group_user.id)],
        })
        session = self._create_session()
        session.coach_id = coach.id
        session.action_confirm()
        with self.assertRaises(UserError):
            session.with_user(self.user).action_mark_in_progress()
        session.with_user(coach).action_mark_in_progress()
        self.assertEqual(session.state, 'in_progress')
        session.with_user(coach).action_mark_done()
        self.assertEqual(session.state, 'done')

    def test_plan_creation_reserved_to_manager(self):
        with self.assertRaises(UserError):
            self.Plan.with_user(self.user).create({
                'code': 'VIP',
                'price_monthly': 80.0,
                'duration_months': 6,
            })
        plan = self.Plan.with_user(self.manager).create({
            'code': 'VIP',
            'price_monthly': 80.0,
            'duration_months': 6,
        })
        self.assertTrue(plan.name.startswith('PLA-'))

    def test_payment_done_sets_subscription_paid(self):
        subscription = self._create_subscription()
        subscription.action_activate()
        payment = self.Payment.create({
            'subscription_id': subscription.id,
            'amount': 150.0,
        })
        payment.action_done()
        self.assertEqual(payment.state, 'done')
        self.assertTrue(subscription.paid)

    def test_payment_done_reserved_to_gym_user_or_manager(self):
        subscription = self._create_subscription()
        payment = self.Payment.create({
            'subscription_id': subscription.id,
            'amount': 150.0,
        })
        with self.assertRaises(UserError):
            payment.with_user(self.plain_user).action_done()
        payment.with_user(self.user).action_done()
        self.assertEqual(payment.state, 'done')

    def test_cron_expire_subscriptions(self):
        subscription = self._create_subscription()
        subscription.action_activate()
        subscription.end_date = fields.Date.today() - timedelta(days=1)
        self.Subscription._cron_expire_subscriptions()
        self.assertEqual(subscription.state, 'expired')

    def test_cron_renewal_alert_dedup(self):
        subscription = self._create_subscription()
        subscription.action_activate()
        subscription.end_date = fields.Date.today() + timedelta(days=3)
        self.env.company.sf_gym_alert_days = 7
        self.Subscription._cron_gym_alerts()
        self.Subscription._cron_gym_alerts()
        todo = self.env.ref('mail.mail_activity_data_todo')
        activities = subscription.activity_ids.filtered(
            lambda a: a.activity_type_id == todo)
        self.assertEqual(len(activities), 1)

    def test_cron_empty_session_alert_dedup(self):
        lesson = self._create_lesson()
        session = self._create_session(lesson=lesson)
        session.date = fields.Date.today() - timedelta(days=1)
        session.action_confirm()
        self.Subscription._cron_gym_alerts()
        self.Subscription._cron_gym_alerts()
        todo = self.env.ref('mail.mail_activity_data_todo')
        activities = session.activity_ids.filtered(
            lambda a: a.activity_type_id == todo)
        self.assertEqual(len(activities), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create(
            {'name': 'Gym Company B'})
        partner = self.env['res.partner'].create({'name': 'Jane Doe'})
        member = self.Member.with_company(company_b).create({
            'partner_id': partner.id,
        })
        found = self.Member.with_user(self.user).search(
            [('id', '=', member.id)])
        self.assertNotIn(member, found)

    def test_reports_render(self):
        member = self._create_member()
        plan = self._create_plan()
        subscription = self._create_subscription(member=member, plan=plan)
        subscription.action_activate()
        report = self.env.ref(
            'sf_gym_fitness.report_sf_gym_subscription_contract')
        result = report._render_qweb_html(subscription.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Subscription Contract', html)
        lesson = self._create_lesson()
        session = self._create_session(lesson=lesson)
        session.action_confirm()
        session_report = self.env.ref(
            'sf_gym_fitness.report_sf_gym_session_planning')
        result = session_report._render_qweb_html(session.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Session Planning', html)
