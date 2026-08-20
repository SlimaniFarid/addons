# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfEvents(TransactionCase):

    def setUp(self):
        super().setUp()
        self.today = fields.Date.today()
        self.todo_type = self.env.ref('mail.mail_activity_data_todo')

    def _create_event(self, company=None, capacity=0, budget=0.0, state='draft', **kwargs):
        vals = {
            'event_type': 'conference',
            'start_date': self.today,
            'end_date': self.today + timedelta(days=1),
            'capacity': capacity,
            'budget': budget,
            'state': state,
            'company_id': (company or self.env.company).id,
        }
        vals.update(kwargs)
        return self.env['sf.event'].create(vals)

    def _create_session(self, event, capacity=0, state='draft', company=None, **kwargs):
        vals = {
            'event_id': event.id,
            'start_datetime': fields.Datetime.now(),
            'end_datetime': fields.Datetime.now() + timedelta(hours=1),
            'capacity': capacity,
            'state': state,
            'company_id': (company or self.env.company).id,
        }
        vals.update(kwargs)
        return self.env['sf.event.session'].create(vals)

    def _create_registration(self, event, price=0.0, state='draft', sessions=None, company=None):
        vals = {
            'event_id': event.id,
            'attendee_name': 'Test Attendee %s' % uuid.uuid4().hex[:6],
            'attendee_email': 'attendee%s@example.com' % uuid.uuid4().hex[:6],
            'ticket_type': 'standard',
            'price_unit': price,
            'state': state,
            'company_id': (company or self.env.company).id,
        }
        if sessions:
            vals['session_ids'] = [(6, 0, [s.id for s in sessions])]
        return self.env['sf.event.registration'].create(vals)

    def _create_expense(self, event, amount=0.0, company=None):
        return self.env['sf.event.expense'].create({
            'event_id': event.id,
            'category': 'venue',
            'amount': amount,
            'company_id': (company or self.env.company).id,
        })

    def _create_user(self, company, manager=False):
        group_xmlid = 'sf_events.group_sf_events_manager' if manager else 'sf_events.group_sf_events_user'
        return self.env['res.users'].create({
            'name': 'Test Manager' if manager else 'Test User',
            'login': 'test_%s_%s' % ('manager' if manager else 'user', uuid.uuid4().hex[:8]),
            'company_id': company.id,
            'company_ids': [(6, 0, [company.id])],
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.env.ref(group_xmlid).id),
            ],
        })

    def _pending_todos(self, record):
        return record.activity_ids.filtered(
            lambda a: a.activity_type_id == self.todo_type and not a.done
        )

    def test_create_sequences(self):
        event = self._create_event()
        session = self._create_session(event)
        registration = self._create_registration(event)
        expense = self._create_expense(event, amount=10.0)
        self.assertTrue(event.name.startswith('EVT-'))
        self.assertTrue(session.name.startswith('SES-'))
        self.assertTrue(registration.name.startswith('REG-'))
        self.assertTrue(expense.name.startswith('EXP-'))

    def test_computed_financials(self):
        event = self._create_event()
        reg1 = self._create_registration(event, price=50.0, state='confirmed')
        reg2 = self._create_registration(event, price=30.0, state='confirmed')
        self._create_expense(event, amount=20.0)
        self.assertEqual(event.revenue, 80.0)
        self.assertEqual(event.expenses_total, 20.0)
        self.assertEqual(event.balance, 60.0)
        reg1.state = 'cancelled'
        self.assertEqual(event.revenue, 30.0)
        self.assertEqual(event.balance, 10.0)

    def test_session_capacity_control(self):
        event = self._create_event()
        session = self._create_session(event, capacity=1)
        reg1 = self._create_registration(event, price=10.0, state='draft', sessions=[session])
        reg1.action_confirm()
        reg2 = self._create_registration(event, price=10.0, state='draft', sessions=[session])
        with self.assertRaises(UserError):
            reg2.action_confirm()

    def test_event_capacity_control(self):
        event = self._create_event(capacity=1)
        reg1 = self._create_registration(event, price=10.0, state='draft')
        reg1.action_confirm()
        reg2 = self._create_registration(event, price=10.0, state='draft')
        with self.assertRaises(UserError):
            reg2.action_confirm()

    def test_session_confirm_on_cancelled_event(self):
        event = self._create_event()
        event.action_cancel()
        session = self._create_session(event)
        with self.assertRaises(UserError):
            session.action_confirm()

    def test_registration_workflow(self):
        event = self._create_event()
        event.action_confirm()
        event.action_start()
        registration = self._create_registration(event, price=10.0, state='draft')
        registration.action_confirm()
        registration.action_check_in()
        self.assertEqual(registration.state, 'checked_in')
        self.assertTrue(registration.check_in_date)
        registration.action_done()
        self.assertEqual(registration.state, 'done')

    def test_check_in_requires_in_progress(self):
        event = self._create_event()
        registration = self._create_registration(event, price=10.0, state='confirmed')
        with self.assertRaises(UserError):
            registration.action_check_in()

    def test_cancel_after_check_in(self):
        event = self._create_event()
        event.action_confirm()
        event.action_start()
        registration = self._create_registration(event, price=10.0, state='confirmed')
        registration.action_check_in()
        with self.assertRaises(UserError):
            registration.action_cancel()

    def test_cancel_event_manager_only(self):
        company = self.env.company
        user = self._create_user(company, manager=False)
        event = self._create_event()
        event.with_user(user).action_cancel()
        with self.assertRaises(UserError):
            event.sudo().with_user(user).action_cancel()

    def test_cron_alerts_dedup(self):
        event = self._create_event(state='confirmed')
        event._cron_daily_alerts()
        event._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(event)), 1)

    def test_multi_company_isolation(self):
        company_a = self.env.company
        company_b = self.env['res.company'].create({'name': 'Test Company B %s' % uuid.uuid4().hex[:6]})
        user = self._create_user(company_a, manager=False)
        event_a = self._create_event(company=company_a)
        event_b = self._create_event(company=company_b)
        self.assertEqual(event_a.with_user(user).name.startswith('EVT-'), True)
        visible = self.env['sf.event'].with_user(user).search([])
        self.assertNotIn(event_b.id, visible.ids)

    def test_multi_company_manager_sees_all(self):
        company_a = self.env.company
        company_b = self.env['res.company'].create({'name': 'Test Company B %s' % uuid.uuid4().hex[:6]})
        manager = self._create_user(company_a, manager=True)
        event_a = self._create_event(company=company_a)
        event_b = self._create_event(company=company_b)
        visible = self.env['sf.event'].with_user(manager).search([])
        self.assertIn(event_a.id, visible.ids)
        self.assertIn(event_b.id, visible.ids)

    def test_confirm_registration_cancelled_event(self):
        event = self._create_event()
        event.action_cancel()
        registration = self._create_registration(event, price=10.0, state='draft')
        with self.assertRaises(UserError):
            registration.action_confirm()

    def test_report_generation(self):
        event = self._create_event(state='confirmed')
        self._create_session(event, state='confirmed')
        registration = self._create_registration(event, price=10.0, state='confirmed')
        self._create_expense(event, amount=5.0)
        for report in ['report_event_program', 'report_registration_confirmation',
                       'report_event_budget', 'report_attendance']:
            action = self.env.ref('sf_events.%s' % report).report_action(registration if report == 'report_registration_confirmation' else event)
            self.assertTrue(action)