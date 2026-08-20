# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfDonations(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Campaign = self.env['sf.donation.campaign']
        self.Promise = self.env['sf.donation.promise']
        self.Payment = self.env['sf.donation.payment']
        self.Receipt = self.env['sf.donation.receipt']
        self.group_user = self.env.ref('sf_donations.group_sf_donation_user')
        self.group_manager = self.env.ref('sf_donations.group_sf_donation_manager')
        self.user = self.env['res.users'].create({
            'name': 'Donation User',
            'login': 'donation_user',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Donation Manager',
            'login': 'donation_manager',
            'groups_id': [(4, self.group_manager.id)],
        })

    def _create_campaign(self):
        return self.Campaign.create({
            'title': 'Winter Drive',
            'target_amount': 5000.0,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=30),
        })

    def _create_promise(self, campaign=None, amount=100.0, donor='John Doe'):
        return self.Promise.create({
            'campaign_id': (campaign or self._create_campaign()).id,
            'donor': donor,
            'amount': amount,
            'pledge_date': fields.Date.today(),
            'frequency': 'once',
        })

    def test_create_records_with_sequences(self):
        campaign = self._create_campaign()
        self.assertTrue(campaign.name.startswith('DON-'))
        promise = self._create_promise(campaign=campaign)
        self.assertTrue(promise.name.startswith('PRM-'))
        promise.action_confirm()
        payment = self.Payment.create({'promise_id': promise.id,
                                       'amount': 100.0})
        self.assertTrue(payment.name.startswith('PAY-'))
        payment.action_receive()
        receipt = self.Receipt.create({'payment_id': payment.id})
        self.assertTrue(receipt.name.startswith('RCP-'))
        self.assertEqual(receipt.amount, payment.amount)

    def test_collected_amount_after_received_payment(self):
        campaign = self._create_campaign()
        promise = self._create_promise(campaign=campaign, amount=100.0)
        promise.action_confirm()
        payment = self.Payment.create({'promise_id': promise.id,
                                       'amount': 100.0})
        self.assertEqual(campaign.collected_amount, 0.0)
        payment.action_receive()
        self.assertEqual(campaign.collected_amount, 100.0)

    def test_promise_paid_when_fully_paid(self):
        promise = self._create_promise(amount=100.0)
        promise.action_confirm()
        self.assertEqual(promise.state, 'pending')
        payment = self.Payment.create({'promise_id': promise.id,
                                       'amount': 100.0})
        payment.action_receive()
        self.assertEqual(promise.state, 'paid')

    def test_payment_received_reserved_to_manager(self):
        promise = self._create_promise()
        promise.action_confirm()
        payment = self.Payment.create({'promise_id': promise.id,
                                       'amount': 50.0})
        with self.assertRaises(UserError):
            payment.with_user(self.user).action_receive()
        payment.with_user(self.manager).action_receive()
        self.assertEqual(payment.state, 'received')

    def test_receipt_issued_reserved_to_manager(self):
        promise = self._create_promise()
        promise.action_confirm()
        payment = self.Payment.create({'promise_id': promise.id,
                                       'amount': 50.0})
        payment.action_receive()
        receipt = self.Receipt.create({'payment_id': payment.id})
        with self.assertRaises(UserError):
            receipt.with_user(self.user).action_issue()
        receipt.with_user(self.manager).action_issue()
        self.assertEqual(receipt.state, 'issued')

    def test_cron_reminder_dedup(self):
        promise = self._create_promise()
        promise.action_confirm()
        promise.pledge_date = fields.Date.today() - timedelta(days=10)
        self.env.company.sf_donation_reminder_days = 7
        promise._cron_donation_reminders()
        promise._cron_donation_reminders()
        todo = self.env.ref('mail.mail_activity_data_todo')
        activities = promise.activity_ids.filtered(
            lambda a: a.activity_type_id == todo)
        self.assertEqual(len(activities), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Donation Company B'})
        user = self.env['res.users'].create({
            'name': 'Donation Company A User',
            'login': 'donation_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        campaign = self._create_campaign()
        promise = self.Promise.with_company(company_b).create({
            'campaign_id': campaign.id,
            'donor': 'Jane Doe',
            'amount': 50.0,
            'pledge_date': fields.Date.today(),
        })
        found = self.Promise.with_user(user).search([('id', '=', promise.id)])
        self.assertNotIn(promise, found)

    def test_reports_render(self):
        campaign = self._create_campaign()
        promise = self._create_promise(campaign=campaign)
        promise.action_confirm()
        payment = self.Payment.create({'promise_id': promise.id,
                                       'amount': 100.0})
        payment.action_receive()
        receipt = self.Receipt.create({'payment_id': payment.id})
        receipt.action_issue()
        report = self.env.ref('sf_donations.report_sf_donation_campaign')
        result = report._render_qweb_html(campaign.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Donation Campaign', html)
        receipt_report = self.env.ref(
            'sf_donations.report_sf_donation_receipt_register')
        result = receipt_report._render_qweb_html(receipt.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Receipt Register', html)