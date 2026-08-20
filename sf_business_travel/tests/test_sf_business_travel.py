# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfBusinessTravel(TransactionCase):

    def setUp(self):
        super().setUp()
        self.employee = self.env.user
        self.user_group = self.env.ref(
            'sf_business_travel.group_sf_business_travel_user')
        self.manager_group = self.env.ref(
            'sf_business_travel.group_sf_business_travel_manager')
        self.todo = self.env.ref('mail.mail_activity_data_todo')

    def _create_travel(self, **kw):
        today = odoo_fields.Date.today()
        vals = {
            'employee_id': self.employee.id,
            'purpose': 'Client meeting',
            'destination': 'Paris',
            'departure_date': today + timedelta(days=5),
            'return_date': today + timedelta(days=8),
            'budget': 500.0,
        }
        vals.update(kw)
        return self.env['sf.business.travel'].create(vals)

    def _create_user(self, group):
        return self.env['res.users'].create({
            'name': 'Travel User',
            'login': 'travel_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [group.id])],
        })

    def test_sequences(self):
        travel = self._create_travel()
        self.assertTrue(travel.name.startswith('TRV-'))
        line = self.env['sf.business.travel.line'].create({
            'travel_id': travel.id,
            'line_type': 'flight',
            'description': 'Flight',
            'amount': 120.0,
        })
        self.assertTrue(line.name.startswith('TRL-'))

    def test_workflow(self):
        travel = self._create_travel()
        travel.action_submit()
        self.assertEqual(travel.state, 'submitted')
        manager = self._create_user(self.manager_group)
        travel.with_user(manager).action_approve()
        self.assertEqual(travel.state, 'approved')
        travel.action_start()
        self.assertEqual(travel.state, 'in_progress')
        travel.action_complete()
        self.assertEqual(travel.state, 'completed')

    def test_reject(self):
        travel = self._create_travel()
        travel.action_submit()
        manager = self._create_user(self.manager_group)
        travel.with_user(manager).action_reject()
        self.assertEqual(travel.state, 'rejected')

    def test_return_before_departure_blocked(self):
        today = odoo_fields.Date.today()
        with self.assertRaises(ValidationError):
            self._create_travel(
                departure_date=today + timedelta(days=5),
                return_date=today + timedelta(days=3))

    def test_estimated_cost(self):
        travel = self._create_travel()
        self.env['sf.business.travel.line'].create({
            'travel_id': travel.id,
            'line_type': 'flight',
            'description': 'Flight',
            'amount': 120.0,
        })
        self.env['sf.business.travel.line'].create({
            'travel_id': travel.id,
            'line_type': 'hotel',
            'description': 'Hotel',
            'amount': 180.0,
        })
        self.assertEqual(travel.estimated_cost, 300.0)

    def test_approval_manager_only(self):
        travel = self._create_travel()
        travel.action_submit()
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            travel.with_user(user).action_approve()

    def test_state_write_guard(self):
        travel = self._create_travel()
        with self.assertRaises(UserError):
            travel.write({'state': 'approved'})

    def test_approved_immutable(self):
        travel = self._create_travel()
        travel.action_submit()
        manager = self._create_user(self.manager_group)
        travel.with_user(manager).action_approve()
        with self.assertRaises(UserError):
            travel.write({'destination': 'Lyon'})

    def test_cancel_own_draft(self):
        travel = self._create_travel()
        user = self._create_user(self.user_group)
        travel.employee_id = user.id
        travel.with_user(user).action_cancel()
        self.assertEqual(travel.state, 'cancelled')

    def test_cancel_foreign_request_blocked(self):
        other = self._create_user(self.user_group)
        travel = self._create_travel(employee_id=other.id)
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            travel.with_user(user).action_cancel()

    def test_cron_reminders(self):
        today = odoo_fields.Date.today()
        upcoming = self._create_travel(
            departure_date=today + timedelta(days=1))
        upcoming.action_submit()
        manager = self._create_user(self.manager_group)
        upcoming.with_user(manager).action_approve()
        far = self._create_travel(
            departure_date=today + timedelta(days=20))
        far.action_submit()
        far.with_user(manager).action_approve()
        self.env['sf.business.travel']._cron_departure_reminders()
        self.assertTrue(upcoming.activity_ids)
        self.assertFalse(far.activity_ids)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({
            'name': 'Travel Co 2'})
        travel2 = self.env['sf.business.travel'].with_company(company2).create({
            'employee_id': self.employee.id,
            'purpose': 'Training',
            'destination': 'Lyon',
            'departure_date': odoo_fields.Date.today(),
            'return_date': odoo_fields.Date.today() + timedelta(days=1),
            'company_id': company2.id,
        })
        user = self._create_user(self.user_group)
        user.write({
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.business.travel'].with_user(user).search(
            [('id', '=', travel2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        travel = self._create_travel()
        travel.action_submit()
        manager = self._create_user(self.manager_group)
        travel.with_user(manager).action_approve()
        for report in ['action_report_travel_authorization',
                       'action_report_travel_itinerary']:
            action = self.env.ref(
                'sf_business_travel.%s' % report).report_action(travel)
            self.assertTrue(action)