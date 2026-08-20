# -*- coding: utf-8 -*-
from datetime import timedelta
import uuid

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfStaffing(TransactionCase):

    def setUp(self):
        super().setUp()
        self.today = fields.Date.today()
        self.todo_type = self.env.ref('mail.mail_activity_data_todo')

    def _create_candidate(self, company=None):
        return self.env['sf.staffing.candidate'].create({
            'name': 'Test Candidate %s' % uuid.uuid4().hex[:6],
            'skills': 'Logistics, Driving',
            'availability': 'immediate',
            'desired_job': 'Warehouse Operator',
            'company_id': (company or self.env.company).id,
        })

    def _create_client(self, company=None):
        partner = self.env['res.partner'].create({'name': 'Client Partner %s' % uuid.uuid4().hex[:6]})
        return self.env['sf.staffing.client'].create({
            'name': 'Test Client %s' % uuid.uuid4().hex[:6],
            'partner_id': partner.id,
            'contact_name': 'Contact Person',
            'company_id': (company or self.env.company).id,
        })

    def _create_need(self, client, company=None):
        return self.env['sf.staffing.need'].create({
            'client_id': client.id,
            'job_title': 'Warehouse Operator',
            'required_skills': 'Logistics',
            'start_date': self.today,
            'end_date': self.today + timedelta(days=10),
            'quantity': 2,
            'company_id': (company or self.env.company).id,
        })

    def _create_mission(self, client, candidate, company=None, end_days=10, hourly_rate=12.5):
        return self.env['sf.staffing.mission'].create({
            'client_id': client.id,
            'candidate_id': candidate.id,
            'start_date': self.today,
            'end_date': self.today + timedelta(days=end_days),
            'hourly_rate': hourly_rate,
            'company_id': (company or self.env.company).id,
        })

    def _create_timesheet(self, mission, date=None, hours=8, state='draft', hourly_rate=None):
        return self.env['sf.staffing.timesheet'].create({
            'mission_id': mission.id,
            'date': date or self.today,
            'hours': hours,
            'hourly_rate': hourly_rate or mission.hourly_rate,
            'state': state,
        })

    def _create_user(self, company, manager=False):
        group_xmlid = 'sf_staffing.group_sf_staffing_manager' if manager else 'sf_staffing.group_sf_staffing_user'
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

    def _create_sale_journal(self, company):
        return self.env['account.journal'].create({
            'name': 'Sales Journal %s' % company.id,
            'type': 'sale',
            'code': 'SALE%s' % company.id,
            'company_id': company.id,
        })

    def _pending_todos(self, record):
        return record.activity_ids.filtered(
            lambda a: a.activity_type_id == self.todo_type and not a.done
        )

    def test_create_sequences(self):
        candidate = self._create_candidate()
        client = self._create_client()
        need = self._create_need(client)
        mission = self._create_mission(client, candidate)
        contract = mission.contract_id
        timesheet = self._create_timesheet(mission)
        self.assertTrue(candidate.name.startswith('CAN-'))
        self.assertTrue(client.name.startswith('CLI-'))
        self.assertTrue(need.name.startswith('NED-'))
        self.assertTrue(mission.name.startswith('MIS-'))
        self.assertTrue(contract.name.startswith('CTR-'))
        self.assertTrue(timesheet.name.startswith('TIM-'))
        self.assertEqual(contract.state, 'draft')

    def test_computed_totals(self):
        candidate = self._create_candidate()
        client = self._create_client()
        mission = self._create_mission(client, candidate, hourly_rate=10)
        timesheet = self._create_timesheet(mission, hours=8)
        self.assertEqual(timesheet.amount, 80.0)
        self.assertEqual(mission.total_billable, 0.0)
        timesheet.action_done()
        self.assertEqual(timesheet.amount, 80.0)
        self.assertEqual(mission.total_billable, 80.0)
        timesheet.write({'hours': 9})
        self.assertEqual(timesheet.amount, 90.0)
        self.assertEqual(mission.total_billable, 90.0)

    def test_user_error_candidate_already_on_mission(self):
        candidate = self._create_candidate()
        client = self._create_client()
        mission_a = self._create_mission(client, candidate)
        mission_a.action_confirm()
        mission_b = self._create_mission(client, candidate)
        with self.assertRaises(UserError):
            mission_b.action_confirm()

    def test_user_error_incoherent_dates(self):
        candidate = self._create_candidate()
        client = self._create_client()
        with self.assertRaises(UserError):
            self._create_mission(client, candidate, end_days=-1)

    def test_user_error_hours_control(self):
        candidate = self._create_candidate()
        client = self._create_client()
        mission = self._create_mission(client, candidate)
        with self.assertRaises(UserError):
            self._create_timesheet(mission, hours=0)
        with self.assertRaises(UserError):
            self._create_timesheet(mission, hours=25)

    def test_user_error_cancel_timesheet_after_done(self):
        candidate = self._create_candidate()
        client = self._create_client()
        mission = self._create_mission(client, candidate)
        mission.action_confirm()
        mission.action_start()
        timesheet = self._create_timesheet(mission)
        timesheet.action_done()
        mission.action_done()
        with self.assertRaises(UserError):
            timesheet.action_cancel()

    def test_mission_workflow(self):
        candidate = self._create_candidate()
        client = self._create_client()
        need = self._create_need(client)
        mission = self._create_mission(client, candidate)
        self.assertEqual(mission.state, 'draft')
        self.assertEqual(mission.contract_id.state, 'draft')
        self.assertEqual(need.state, 'open')
        mission.action_confirm()
        self.assertEqual(mission.state, 'confirmed')
        self.assertEqual(mission.contract_id.state, 'confirmed')
        self.assertEqual(candidate.state, 'on_mission')
        self.assertEqual(need.state, 'assigned')
        mission.action_start()
        self.assertEqual(mission.state, 'in_progress')
        mission.action_done()
        self.assertEqual(mission.state, 'done')
        self.assertEqual(mission.contract_id.state, 'done')
        self.assertEqual(candidate.state, 'available')
        self.assertEqual(need.state, 'filled')

    def test_invoicing_only_done(self):
        journal = self._create_sale_journal(self.env.company)
        candidate = self._create_candidate()
        client = self._create_client()
        mission = self._create_mission(client, candidate, hourly_rate=10)
        mission.action_confirm()
        self._create_timesheet(mission, hours=5, state='draft')
        self._create_timesheet(mission, hours=4, state='confirmed')
        self._create_timesheet(mission, hours=8, state='done')
        self.assertEqual(mission.total_billable, 80.0)
        mission.action_create_invoice()
        self.assertEqual(len(mission.invoice_ids), 1)
        invoice = mission.invoice_ids[0]
        self.assertEqual(invoice.move_type, 'out_invoice')
        self.assertEqual(len(invoice.invoice_line_ids), 1)
        self.assertEqual(invoice.invoice_line_ids.quantity, 8.0)
        self.assertEqual(invoice.invoice_line_ids.price_unit, 10.0)

    def test_manager_only_actions(self):
        candidate = self._create_candidate()
        client = self._create_client()
        mission = self._create_mission(client, candidate)
        mission.action_confirm()
        user = self._create_user(self.env.company, manager=False)
        manager = self._create_user(self.env.company, manager=True)
        with self.assertRaises(UserError):
            mission.with_user(user).action_cancel()
        with self.assertRaises(UserError):
            mission.contract_id.with_user(user).write({'hourly_rate': 20})
        mission.contract_id.with_user(manager).write({'hourly_rate': 20})
        mission.with_user(manager).action_cancel()
        self.assertEqual(mission.state, 'cancelled')
        self.assertEqual(mission.contract_id.state, 'cancelled')

    def test_cron_dedup(self):
        candidate = self._create_candidate()
        client = self._create_client()
        mission = self._create_mission(client, candidate, end_days=2)
        mission.action_confirm()
        timesheet = self._create_timesheet(mission, date=self.today - timedelta(days=1), state='draft')
        done_timesheet = self._create_timesheet(mission, date=self.today - timedelta(days=1), state='done')
        self.env['sf.staffing.mission']._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(mission)), 1)
        self.assertEqual(len(self._pending_todos(timesheet)), 1)
        self.assertEqual(len(self._pending_todos(done_timesheet)), 0)
        self.env['sf.staffing.mission']._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(mission)), 1)
        self.assertEqual(len(self._pending_todos(timesheet)), 1)

    def test_multi_company(self):
        company_b = self.env['res.company'].create({'name': 'Test Company B'})
        self.env.user.write({
            'company_ids': [(6, 0, (self.env.company | company_b).ids)],
        })
        candidate_a = self._create_candidate(company=self.env.company)
        client_a = self._create_client(company=self.env.company)
        candidate_b = self._create_candidate(company=company_b)
        client_b = self._create_client(company=company_b)
        mission_a = self._create_mission(client_a, candidate_a, company=self.env.company, end_days=2)
        mission_a.action_confirm()
        mission_b = self._create_mission(client_b, candidate_b, company=company_b, end_days=2)
        mission_b.action_confirm()
        self.assertEqual(mission_a.company_id, self.env.company)
        self.assertEqual(mission_b.company_id, company_b)
        self.assertEqual(mission_a.contract_id.company_id, self.env.company)
        self.assertEqual(mission_b.contract_id.company_id, company_b)
        user = self._create_user(self.env.company, manager=False)
        user_env = self.env(user=user)
        visible = user_env['sf.staffing.mission'].search([])
        self.assertIn(mission_a, visible)
        self.assertNotIn(mission_b, visible)
        manager = self._create_user(self.env.company, manager=True)
        manager_env = self.env(user=manager)
        visible_manager = manager_env['sf.staffing.mission'].search([])
        self.assertIn(mission_a, visible_manager)
        self.assertIn(mission_b, visible_manager)

    def test_cron_multi_company(self):
        company_b = self.env['res.company'].create({'name': 'Test Company B'})
        self.env.user.write({
            'company_ids': [(6, 0, (self.env.company | company_b).ids)],
        })
        candidate_a = self._create_candidate(company=self.env.company)
        client_a = self._create_client(company=self.env.company)
        candidate_b = self._create_candidate(company=company_b)
        client_b = self._create_client(company=company_b)
        mission_a = self._create_mission(client_a, candidate_a, company=self.env.company, end_days=2)
        mission_a.action_confirm()
        mission_b = self._create_mission(client_b, candidate_b, company=company_b, end_days=2)
        mission_b.action_confirm()
        ts_b = self._create_timesheet(mission_b, date=self.today - timedelta(days=1), state='draft')
        self.env['sf.staffing.mission']._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(mission_a)), 1)
        self.assertEqual(len(self._pending_todos(mission_b)), 1)
        self.assertEqual(len(self._pending_todos(ts_b)), 1)

    def test_pdf_reports(self):
        candidate = self._create_candidate()
        client = self._create_client()
        need = self._create_need(client)
        mission = self._create_mission(client, candidate, hourly_rate=10)
        mission.action_confirm()
        timesheet = self._create_timesheet(mission, hours=8, state='done')
        contract = mission.contract_id
        report = self.env['ir.actions.report']
        for report_ref, records in [
            ('sf_staffing.report_sf_staffing_contract', contract),
            ('sf_staffing.report_sf_staffing_candidate', candidate),
            ('sf_staffing.report_sf_staffing_mission_invoice', mission),
            ('sf_staffing.report_sf_staffing_activity', mission),
        ]:
            content, report_format = report._render_qweb_pdf(report_ref, records.ids)
            self.assertTrue(content)
            self.assertIsInstance(content, bytes)
            self.assertTrue(len(content) > 0)