# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfSalonBeauty(TransactionCase):

    def setUp(self):
        super().setUp()
        self.todo_type = self.env.ref('mail.mail_activity_data_todo')
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.staff_partner = self.env['res.partner'].create({
            'name': 'Staff Partner %s' % uuid.uuid4().hex[:6],
        })
        self.product = self.env['product.product'].create({
            'name': 'Haircut Product %s' % uuid.uuid4().hex[:6],
            'type': 'service',
        })
        self.service = self.env['sf.salon.service'].create({
            'name': 'Haircut',
            'category': 'haircut',
            'duration': 30,
            'price': 40.0,
            'commission_rate': 10.0,
            'product_id': self.product.id,
        })
        self.staff = self.env['sf.salon.staff'].create({
            'name': 'Mehdi',
            'partner_id': self.staff_partner.id,
            'commission_rate': 10.0,
            'service_ids': [(6, 0, [self.service.id])],
        })

    def _create_appointment(self, start=None, staff=None, service=None, state='draft'):
        vals = {
            'partner_id': self.customer.id,
            'staff_id': (staff or self.staff).id,
            'service_id': (service or self.service).id,
            'start_datetime': start or fields.Datetime.now(),
            'state': state,
        }
        return self.env['sf.salon.appointment'].create(vals)

    def _pending_todos(self, record):
        return record.activity_ids.filtered(
            lambda a: a.activity_type_id == self.todo_type and not a.done
        )

    def test_sequences(self):
        appointment = self._create_appointment()
        package = self.env['sf.salon.package'].create({
            'partner_id': self.customer.id,
            'service_id': self.service.id,
            'sessions_total': 5,
            'amount': 180.0,
        })
        self.assertTrue(appointment.name.startswith('RDV-'))
        self.assertTrue(package.name.startswith('FRF-'))

    def test_appointment_workflow(self):
        appointment = self._create_appointment()
        appointment.action_confirm()
        self.assertEqual(appointment.state, 'confirmed')
        appointment.action_start()
        self.assertEqual(appointment.state, 'in_progress')
        appointment.action_done()
        self.assertEqual(appointment.state, 'done')
        self.assertTrue(appointment.invoice_id)

    def test_conflict_detection(self):
        start = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        appointment = self._create_appointment(start=start)
        appointment.action_confirm()
        conflict = self._create_appointment(start=start + timedelta(minutes=15))
        with self.assertRaises(UserError):
            conflict.action_confirm()

    def test_no_conflict_when_free(self):
        start = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        appointment = self._create_appointment(start=start)
        appointment.action_confirm()
        later = self._create_appointment(start=start + timedelta(hours=2))
        later.action_confirm()
        self.assertEqual(later.state, 'confirmed')

    def test_package_consumption(self):
        package = self.env['sf.salon.package'].create({
            'partner_id': self.customer.id,
            'service_id': self.service.id,
            'sessions_total': 2,
            'amount': 70.0,
        })
        self.assertEqual(package.sessions_left, 2)
        package._consume_session()
        self.assertEqual(package.sessions_used, 1)
        self.assertEqual(package.state, 'partially_used')
        package._consume_session()
        self.assertEqual(package.state, 'exhausted')
        with self.assertRaises(UserError):
            package._consume_session()

    def test_expired_package_blocked(self):
        package = self.env['sf.salon.package'].create({
            'partner_id': self.customer.id,
            'service_id': self.service.id,
            'sessions_total': 1,
            'expiration_date': fields.Date.today(),
        })
        package._cron_daily_expirations()
        self.assertEqual(package.state, 'expired')
        with self.assertRaises(UserError):
            package._consume_session()

    def test_commission_calculation(self):
        start = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        appointment = self._create_appointment(start=start)
        appointment.action_confirm()
        appointment.action_start()
        appointment.action_done()
        commission = self.env['sf.salon.commission'].create({
            'period': start.strftime('%Y-%m'),
            'staff_id': self.staff.id,
        })
        commission.action_compute()
        self.assertEqual(commission.state, 'computed')
        self.assertEqual(commission.amount, 4.0)

    def test_no_show_no_commission(self):
        start = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
        appointment = self._create_appointment(start=start)
        appointment.action_confirm()
        appointment.action_no_show()
        self.assertEqual(appointment.state, 'no_show')
        commission = self.env['sf.salon.commission'].create({
            'period': start.strftime('%Y-%m'),
            'staff_id': self.staff.id,
        })
        commission.action_compute()
        self.assertEqual(commission.amount, 0.0)

    def test_done_appointment_immutable(self):
        appointment = self._create_appointment()
        appointment.action_confirm()
        appointment.action_start()
        appointment.action_done()
        with self.assertRaises(UserError):
            appointment.action_cancel()

    def test_report_generation(self):
        appointment = self._create_appointment()
        appointment.action_confirm()
        appointment.action_start()
        appointment.action_done()
        for report in ['action_report_customer_card', 'action_report_activity']:
            action = self.env.ref('sf_salon_beauty.%s' % report).report_action(appointment)
            self.assertTrue(action)
        commission = self.env['sf.salon.commission'].create({
            'period': appointment.start_datetime.strftime('%Y-%m'),
            'staff_id': self.staff.id,
        })
        commission.action_compute()
        action = self.env.ref('sf_salon_beauty.action_report_commissions').report_action(commission)
        self.assertTrue(action)

    def test_refunded_package_blocked(self):
        package = self.env['sf.salon.package'].create({
            'partner_id': self.customer.id,
            'service_id': self.service.id,
            'sessions_total': 2,
            'amount': 70.0,
        })
        package.action_refund()
        self.assertEqual(package.state, 'refunded')
        with self.assertRaises(UserError):
            package._consume_session()

    def test_settings_defaults_applied(self):
        self.env['ir.config_parameter'].sudo().set_param('sf_salon_beauty.default_duration', '60')
        self.env['ir.config_parameter'].sudo().set_param('sf_salon_beauty.default_commission_rate', '5.0')
        service = self.env['sf.salon.service'].create({
            'name': 'Default Duration Service',
            'category': 'other',
            'price': 20.0,
            'product_id': self.product.id,
        })
        staff = self.env['sf.salon.staff'].create({
            'name': 'Default Rate Staff',
            'partner_id': self.staff_partner.id,
        })
        self.assertEqual(service.duration, 60)
        self.assertEqual(staff.commission_rate, 5.0)

    def test_multi_company_commission_isolation(self):
        company_b = self.env['res.company'].create({'name': 'Company B %s' % uuid.uuid4().hex[:6]})
        env_b = self.env.with_company(company_b)
        service_b = env_b['sf.salon.service'].create({
            'name': 'Manicure B',
            'category': 'manicure',
            'duration': 45,
            'price': 30.0,
            'commission_rate': 20.0,
            'product_id': self.product.id,
        })
        staff_b = env_b['sf.salon.staff'].create({
            'name': 'Staff B',
            'partner_id': self.staff_partner.id,
            'commission_rate': 20.0,
            'service_ids': [(6, 0, [service_b.id])],
        })
        start = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
        appointment_b = env_b['sf.salon.appointment'].create({
            'partner_id': self.customer.id,
            'staff_id': staff_b.id,
            'service_id': service_b.id,
            'start_datetime': start,
        })
        appointment_b.action_confirm()
        appointment_b.action_start()
        appointment_b.action_done()
        self.assertEqual(appointment_b.company_id.id, company_b.id)
        commission_b = env_b['sf.salon.commission'].create({
            'period': start.strftime('%Y-%m'),
            'staff_id': staff_b.id,
        })
        commission_b.action_compute()
        self.assertEqual(commission_b.amount, 6.0)
        commission_a = self.env['sf.salon.commission'].create({
            'period': start.strftime('%Y-%m'),
            'staff_id': self.staff.id,
        })
        commission_a.action_compute()
        self.assertEqual(commission_a.amount, 0.0)

    def test_record_rule_company_isolation(self):
        company_b = self.env['res.company'].create({'name': 'Company B %s' % uuid.uuid4().hex[:6]})
        user_b = self.env['res.users'].create({
            'name': 'Salon User B',
            'login': 'salon_user_%s' % uuid.uuid4().hex[:6],
            'email': 'salon_user_%s@example.com' % uuid.uuid4().hex[:6],
            'password': 'salon_user_password',
            'groups_id': [(6, 0, [self.env.ref('sf_salon_beauty.group_sf_salon_user').id])],
            'company_ids': [(6, 0, [company_b.id])],
            'company_id': company_b.id,
        })
        appointment = self._create_appointment()
        appointment.action_confirm()
        env_user = self.env(user=user_b, company_id=company_b.id)
        visible = env_user['sf.salon.appointment'].search([('id', '=', appointment.id)])
        self.assertFalse(visible)