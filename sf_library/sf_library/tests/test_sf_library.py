# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfLibrary(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Category = self.env['sf.library.category']
        self.Item = self.env['sf.library.item']
        self.Member = self.env['sf.library.member']
        self.Loan = self.env['sf.library.loan']
        self.Reservation = self.env['sf.library.reservation']
        self.group_user = self.env.ref('sf_library.group_sf_library_user')
        self.group_manager = self.env.ref('sf_library.group_sf_library_manager')
        self.user = self.env['res.users'].create({
            'name': 'Library User',
            'login': 'library_user',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Library Manager',
            'login': 'library_manager',
            'groups_id': [(4, self.group_manager.id)],
        })

    def _create_category(self, name=None):
        vals = {}
        if name:
            vals['name'] = name
        return self.Category.create(vals)

    def _create_item(self, name='Dune', total_copies=1, category=None):
        return self.Item.create({
            'name': name,
            'author': 'Frank Herbert',
            'total_copies': total_copies,
            'category_id': (category or self._create_category('Fiction')).id,
        })

    def _create_member(self, email='member@example.com'):
        return self.Member.create({'email': email})

    def _create_loan(self, item=None, member=None, loan_date=None):
        return self.Loan.create({
            'item_id': (item or self._create_item()).id,
            'member_id': (member or self._create_member()).id,
            'loan_date': loan_date or fields.Date.today(),
        })

    def test_create_records_with_sequences(self):
        category = self._create_category()
        self.assertTrue(category.name.startswith('CAT-'))
        item = self._create_item(total_copies=2)
        self.assertTrue(item.reference.startswith('LIB-'))
        member = self._create_member()
        self.assertTrue(member.name.startswith('MEM-'))
        member.action_activate()
        loan = self._create_loan(item=item, member=member)
        self.assertTrue(loan.name.startswith('LOA-'))
        loan.action_confirm()
        self.assertEqual(loan.state, 'on_loan')
        self.assertEqual(loan.due_date, loan.loan_date + timedelta(days=21))
        reservation = self.Reservation.create({
            'item_id': item.id,
            'member_id': member.id,
        })
        self.assertTrue(reservation.name.startswith('RES-'))
        self.assertEqual(reservation.status, 'ready')
        self.assertTrue(reservation.expiry_date)

    def test_available_copies_late_days_late_fee(self):
        item = self._create_item(total_copies=2)
        member = self._create_member()
        member.action_activate()
        self.assertEqual(item.available_copies, 2)
        loan = self._create_loan(item=item, member=member)
        loan.action_confirm()
        self.assertEqual(item.available_copies, 1)
        loan.loan_date = fields.Date.today() - timedelta(days=30)
        loan.due_date = fields.Date.today() - timedelta(days=10)
        loan.action_return()
        self.assertEqual(loan.state, 'returned')
        self.assertEqual(loan.late_days, 10)
        self.assertEqual(loan.late_fee, 5.0)

    def test_loan_availability_control(self):
        item = self._create_item(total_copies=1)
        member_a = self._create_member()
        member_b = self._create_member('second@example.com')
        member_a.action_activate()
        member_b.action_activate()
        loan_a = self._create_loan(item=item, member=member_a)
        loan_a.action_confirm()
        loan_b = self._create_loan(item=item, member=member_b)
        with self.assertRaises(UserError):
            loan_b.action_confirm()

    def test_return_block_fulfil_cancel_reserved_to_manager(self):
        item = self._create_item(total_copies=2)
        member = self._create_member()
        member.action_activate()
        loan = self._create_loan(item=item, member=member)
        loan.action_confirm()
        with self.assertRaises(UserError):
            loan.with_user(self.user).action_return()
        loan.with_user(self.manager).action_return()
        self.assertEqual(loan.state, 'returned')
        member_b = self._create_member('block@example.com')
        member_b.action_activate()
        with self.assertRaises(UserError):
            member_b.with_user(self.user).action_block()
        member_b.with_user(self.manager).action_block()
        self.assertEqual(member_b.status, 'blocked')
        reservation = self.Reservation.create({
            'item_id': item.id,
            'member_id': member.id,
        })
        self.assertEqual(reservation.status, 'ready')
        with self.assertRaises(UserError):
            reservation.with_user(self.user).action_fulfil()
        reservation.with_user(self.manager).action_fulfil()
        self.assertEqual(reservation.status, 'fulfilled')

    def test_blocked_member_cannot_loan(self):
        item = self._create_item(total_copies=1)
        member = self._create_member()
        member.action_activate()
        member.with_user(self.manager).action_block()
        self.assertEqual(member.status, 'blocked')
        loan = self._create_loan(item=item, member=member)
        with self.assertRaises(UserError):
            loan.action_confirm()

    def test_cron_alerts_dedup(self):
        item = self._create_item(total_copies=1)
        member = self._create_member()
        member.action_activate()
        loan = self._create_loan(item=item, member=member)
        loan.action_confirm()
        loan.due_date = fields.Date.today() - timedelta(days=1)
        loan._cron_library_alerts()
        loan._cron_library_alerts()
        todo = self.env.ref('mail.mail_activity_data_todo')
        activities = loan.activity_ids.filtered(
            lambda a: a.activity_type_id == todo)
        self.assertEqual(len(activities), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'Library Company B'})
        item = self._create_item(total_copies=1)
        member = self._create_member()
        loan = self.Loan.with_company(company_b).create({
            'item_id': item.id,
            'member_id': member.id,
            'loan_date': fields.Date.today(),
        })
        found = self.Loan.with_user(self.user).search([('id', '=', loan.id)])
        self.assertNotIn(loan, found)

    def test_reports_render(self):
        item = self._create_item(total_copies=1)
        member = self._create_member()
        member.action_activate()
        loan = self._create_loan(item=item, member=member)
        loan.action_confirm()
        loan.due_date = fields.Date.today() - timedelta(days=5)
        loan.action_return()
        loan_report = self.env.ref('sf_library.report_sf_library_loan_receipt')
        result = loan_report._render_qweb_html(loan.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Loan Receipt', html)
        late_report = self.env.ref('sf_library.report_sf_library_late_report')
        result = late_report._render_qweb_html(loan.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Late Loans &amp; Sanctions', html)
