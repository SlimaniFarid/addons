# -*- coding: utf-8 -*-
from datetime import timedelta
from uuid import uuid4

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfTravelAgency(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True, no_reset_password=True))
        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer %s' % uuid4()})
        cls.package_obj = cls.env['sf.travel.package']
        cls.provider_obj = cls.env['sf.travel.provider']
        cls.reservation_obj = cls.env['sf.travel.reservation']
        cls.cost_obj = cls.env['sf.travel.provider.cost']

    def _create_package(self, **kwargs):
        vals = {
            'destination': 'Paris %s' % uuid4(),
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=7),
            'price_unit': 1000.0,
            'capacity': 10,
        }
        vals.update(kwargs)
        return self.package_obj.create(vals)

    def _create_provider(self, **kwargs):
        vals = {
            'provider_type': 'hotel',
            'partner_id': self.partner.id,
            'contract_ref': 'REF-%s' % uuid4(),
        }
        vals.update(kwargs)
        return self.provider_obj.create(vals)

    def _create_reservation(self, package, **kwargs):
        vals = {
            'package_id': package.id,
            'partner_id': self.partner.id,
            'traveler_name': 'Traveler %s' % uuid4(),
            'traveler_email': 'traveler_%s@example.com' % uuid4(),
            'pax': 1,
            'price_unit': 1000.0,
        }
        vals.update(kwargs)
        return self.reservation_obj.create(vals)

    def _create_cost(self, reservation, amount=100.0):
        provider = self._create_provider()
        return self.cost_obj.create({
            'reservation_id': reservation.id,
            'provider_id': provider.id,
            'amount': amount,
        })

    def _create_user(self, manager=False):
        group = 'sf_travel_agency.group_sf_travel_agency_manager' if manager else 'sf_travel_agency.group_sf_travel_agency_user'
        return self.env['res.users'].create({
            'name': 'User %s' % uuid4(),
            'login': 'user_%s' % uuid4(),
            'group_ids': [(6, 0, [self.env.ref(group).id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })

    def test_sequence_prefix_package(self):
        package = self._create_package()
        self.assertTrue(package.name.startswith('PKG-'))

    def test_sequence_prefix_provider(self):
        provider = self._create_provider()
        self.assertTrue(provider.name.startswith('PRV-'))

    def test_sequence_prefix_reservation(self):
        reservation = self._create_reservation(self._create_package())
        self.assertTrue(reservation.name.startswith('RSV-'))

    def test_sequence_prefix_provider_cost(self):
        cost = self._create_cost(self._create_reservation(self._create_package()))
        self.assertTrue(cost.name.startswith('CST-'))

    def test_computed_cost_commission_margin(self):
        reservation = self._create_reservation(self._create_package(), price_unit=1000.0)
        self.assertEqual(reservation.cost, 0.0)
        self.assertEqual(reservation.commission, 100.0)
        self.assertEqual(reservation.margin, 1000.0)
        cost = self._create_cost(reservation, amount=300.0)
        self.assertEqual(reservation.cost, 300.0)
        self.assertEqual(reservation.margin, 700.0)

    def test_computed_recompute_on_cost_write(self):
        reservation = self._create_reservation(self._create_package(), price_unit=1000.0)
        cost = self._create_cost(reservation, amount=200.0)
        self.assertEqual(reservation.cost, 200.0)
        cost.write({'amount': 500.0})
        self.assertEqual(reservation.cost, 500.0)
        self.assertEqual(reservation.margin, 500.0)
        self._create_cost(reservation, amount=100.0)
        self.assertEqual(reservation.cost, 600.0)

    def test_capacity_reached(self):
        package = self._create_package(capacity=4)
        reservation = self._create_reservation(package, pax=3)
        reservation.action_confirm()
        other = self._create_reservation(package, pax=2)
        with self.assertRaises(UserError):
            other.action_confirm()

    def test_incoherent_dates(self):
        with self.assertRaises(UserError):
            self._create_package(
                start_date=fields.Date.today() + timedelta(days=10),
                end_date=fields.Date.today() + timedelta(days=5),
            )

    def test_confirm_closed_package(self):
        package = self._create_package()
        package.action_close()
        reservation = self._create_reservation(package)
        with self.assertRaises(UserError):
            reservation.action_confirm()

    def test_confirm_cancelled_package(self):
        package = self._create_package()
        package.action_cancel()
        reservation = self._create_reservation(package)
        with self.assertRaises(UserError):
            reservation.action_confirm()

    def test_cancel_after_completed(self):
        reservation = self._create_reservation(self._create_package())
        reservation.action_confirm()
        reservation.action_paid()
        reservation.action_completed()
        with self.assertRaises(UserError):
            reservation.action_cancel()

    def test_workflow_full(self):
        reservation = self._create_reservation(self._create_package())
        self.assertEqual(reservation.state, 'draft')
        reservation.action_confirm()
        self.assertEqual(reservation.state, 'confirmed')
        reservation.action_paid()
        self.assertEqual(reservation.state, 'paid')
        reservation.action_completed()
        self.assertEqual(reservation.state, 'completed')

    def test_workflow_cancel_from_draft(self):
        reservation = self._create_reservation(self._create_package())
        reservation.action_cancel()
        self.assertEqual(reservation.state, 'cancelled')

    def test_confirmation_activity_created(self):
        reservation = self._create_reservation(self._create_package())
        reservation.action_confirm()
        self.assertTrue(reservation.activity_ids)

    def test_archived_provider_not_added(self):
        provider = self._create_provider()
        provider.action_archive()
        package = self._create_package()
        with self.assertRaises(UserError):
            package.write({'provider_ids': [(4, provider.id)]})

    def test_manager_price_write(self):
        package = self._create_package()
        user = self._create_user(manager=False)
        with self.assertRaises(UserError):
            package.with_user(user).write({'price_unit': 2000.0})

    def test_cancel_paid_manager_only(self):
        reservation = self._create_reservation(self._create_package())
        reservation.action_confirm()
        reservation.action_paid()
        user = self._create_user(manager=False)
        with self.assertRaises(UserError):
            reservation.with_user(user).action_cancel()
        manager = self._create_user(manager=True)
        reservation.with_user(manager).action_cancel()
        self.assertEqual(reservation.state, 'cancelled')

    def test_archive_provider_manager_only(self):
        provider = self._create_provider()
        user = self._create_user(manager=False)
        with self.assertRaises(UserError):
            provider.with_user(user).action_archive()
        manager = self._create_user(manager=True)
        provider.with_user(manager).action_archive()
        self.assertFalse(provider.active)
        self.assertEqual(provider.state, 'archived')

    def test_cron_departure_alert(self):
        package = self._create_package(start_date=fields.Date.today() + timedelta(days=3))
        self.env['sf.travel.package']._cron_departure_and_unpaid_alerts()
        self.assertTrue(package.activity_ids)

    def test_cron_departure_alert_dedup(self):
        package = self._create_package(start_date=fields.Date.today() + timedelta(days=3))
        self.env['sf.travel.package']._cron_departure_and_unpaid_alerts()
        self.env['sf.travel.package']._cron_departure_and_unpaid_alerts()
        self.assertEqual(len(package.activity_ids), 1)

    def test_cron_unpaid_alert(self):
        package = self._create_package()
        reservation = self._create_reservation(package, booking_date=fields.Date.today() - timedelta(days=3))
        reservation.action_confirm()
        self.env['sf.travel.package']._cron_departure_and_unpaid_alerts()
        self.assertTrue(reservation.activity_ids)

    def test_cron_unpaid_alert_dedup(self):
        package = self._create_package()
        reservation = self._create_reservation(package, booking_date=fields.Date.today() - timedelta(days=3))
        reservation.action_confirm()
        self.env['sf.travel.package']._cron_departure_and_unpaid_alerts()
        self.env['sf.travel.package']._cron_departure_and_unpaid_alerts()
        unpaid = reservation.activity_ids.filtered(lambda act: act.summary.startswith('Unpaid reservation'))
        self.assertEqual(len(unpaid), 1)

    def test_multicompany_isolation(self):
        company_b = self.env['res.company'].create({'name': 'Company B %s' % uuid4()})
        package_a = self._create_package()
        package_b = self.package_obj.with_company(company_b).create({
            'destination': 'Rome %s' % uuid4(),
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=7),
            'price_unit': 900.0,
            'capacity': 5,
        })
        user = self._create_user(manager=False)
        visible = self.package_obj.with_user(user).search([])
        self.assertIn(package_a, visible)
        self.assertNotIn(package_b, visible)

    def test_multicompany_cron(self):
        company_b = self.env['res.company'].create({'name': 'Company B %s' % uuid4()})
        package_b = self.package_obj.with_company(company_b).create({
            'destination': 'Rome %s' % uuid4(),
            'start_date': fields.Date.today() + timedelta(days=2),
            'end_date': fields.Date.today() + timedelta(days=9),
            'price_unit': 900.0,
            'capacity': 5,
        })
        self.env['sf.travel.package']._cron_departure_and_unpaid_alerts()
        self.assertTrue(package_b.activity_ids)

    def test_report_html_reservation_confirmation(self):
        reservation = self._create_reservation(self._create_package())
        reservation.action_confirm()
        report = self.env.ref('sf_travel_agency.action_report_reservation_confirmation')
        html, _ = report._render_qweb_html(reservation.ids)
        self.assertIn('Reservation Confirmation', html)

    def test_report_html_package_itinerary(self):
        package = self._create_package()
        report = self.env.ref('sf_travel_agency.action_report_package_itinerary')
        html, _ = report._render_qweb_html(package.ids)
        self.assertIn('Package Itinerary', html)

    def test_report_html_reservation_invoice(self):
        reservation = self._create_reservation(self._create_package())
        report = self.env.ref('sf_travel_agency.action_report_reservation_invoice')
        html, _ = report._render_qweb_html(reservation.ids)
        self.assertIn('Reservation Invoice', html)

    def test_report_html_margin_report(self):
        reservation = self._create_reservation(self._create_package())
        report = self.env.ref('sf_travel_agency.action_report_margin_report')
        html, _ = report._render_qweb_html(reservation.ids)
        self.assertIn('Margin Report', html)

    def test_report_pdf_generation(self):
        reservation = self._create_reservation(self._create_package())
        reservation.action_confirm()
        report = self.env.ref('sf_travel_agency.action_report_reservation_confirmation')
        content, _ = report._render_qweb_pdf(reservation.ids)
        self.assertTrue(content)
