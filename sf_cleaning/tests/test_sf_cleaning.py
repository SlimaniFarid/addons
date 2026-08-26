# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfCleaning(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Contract = self.env['sf.cleaning.contract']
        self.ContractLine = self.env['sf.cleaning.contract.line']
        self.Site = self.env['sf.cleaning.site']
        self.Schedule = self.env['sf.cleaning.schedule']
        self.ScheduleLine = self.env['sf.cleaning.schedule.line']
        self.QualityCheck = self.env['sf.cleaning.quality_check']
        self.group_user = self.env.ref('sf_cleaning.group_sf_cleaning_user')
        self.group_manager = self.env.ref(
            'sf_cleaning.group_sf_cleaning_manager')
        self.partner = self.env['res.partner'].create({
            'name': 'Cleaning Client',
        })
        self.user = self.env['res.users'].create({
            'name': 'Cleaning User',
            'login': 'cleaning_user',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Cleaning Manager',
            'login': 'cleaning_manager',
            'groups_id': [(4, self.group_manager.id)],
        })

    def _create_site(self):
        return self.Site.create({
            'name': 'Head Office',
            'partner_id': self.partner.id,
            'area_m2': 500.0,
        })

    def _create_contract(self, site=None, with_line=True):
        contract = self.Contract.create({
            'partner_id': self.partner.id,
            'contract_type': 'recurring',
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + timedelta(days=365),
            'billing_period': 'monthly',
        })
        if with_line:
            self.ContractLine.create({
                'contract_id': contract.id,
                'site_id': (site or self._create_site()).id,
                'cleaning_type': 'standard',
                'frequency': 'weekly',
                'planned_qty': 1.0,
                'unit_price': 50.0,
            })
        return contract

    def _create_schedule(self, contract=None, site=None, agent=None,
                         planned_date=None):
        if not contract:
            site = site or self._create_site()
            contract = self._create_contract(site=site)
        return self.Schedule.create({
            'contract_id': contract.id,
            'site_id': (site or contract.line_ids[0].site_id).id,
            'agent_id': agent.id if agent else False,
            'planned_date': planned_date or fields.Date.today(),
        })

    def _create_line(self, schedule, agent=None, planned_date=None):
        return self.ScheduleLine.create({
            'schedule_id': schedule.id,
            'task': 'Standard cleaning',
            'planned_date': planned_date or fields.Date.today(),
            'agent_id': agent.id if agent else False,
        })

    def test_create_records_with_sequences(self):
        site = self._create_site()
        contract = self._create_contract(site=site)
        self.assertTrue(contract.name.startswith('CLN-'))
        schedule = self._create_schedule(contract=contract, site=site)
        self.assertTrue(schedule.name.startswith('SCH-'))
        line = self._create_line(schedule)
        line.action_mark_done()
        check = self.QualityCheck.create({
            'schedule_line_id': line.id,
            'rating': '5',
        })
        self.assertTrue(check.name.startswith('QC-'))

    def test_stored_computations(self):
        today = fields.Date.today()
        site = self._create_site()
        contract = self._create_contract(site=site)
        contract_line = contract.line_ids.filtered(
            lambda l: l.site_id == site)
        self.assertEqual(contract_line.interval_days, 7)
        schedule = self._create_schedule(contract=contract, site=site,
                                         planned_date=today)
        line = self._create_line(schedule, planned_date=today)
        self.assertEqual(line.prochaine_date_prevue, today + timedelta(days=7))
        check = self.QualityCheck.create({
            'schedule_line_id': line.id,
            'check_date': today - timedelta(days=5),
            'rating': '3',
        })
        self.assertEqual(contract.overdue_quality_check_count, 1)
        line.action_mark_done()
        schedule.action_start()
        schedule.action_submit()
        schedule.action_validate()
        self.assertEqual(site.validated_intervention_count, 1)
        check.action_validate()
        self.assertEqual(check.state, 'done')

    def test_agent_double_assignment_error(self):
        site = self._create_site()
        contract = self._create_contract(site=site)
        schedule = self._create_schedule(contract=contract, site=site)
        agent = self.user
        self._create_line(schedule, agent=agent)
        with self.assertRaises(UserError):
            self._create_line(schedule, agent=agent)

    def test_validation_without_quality_check_error(self):
        schedule = self._create_schedule()
        line = self._create_line(schedule)
        line.action_mark_done()
        schedule.action_start()
        schedule.action_submit()
        with self.assertRaises(UserError):
            schedule.action_validate()
        check = self.QualityCheck.create({
            'schedule_line_id': line.id,
            'rating': '4',
        })
        check.action_validate()
        schedule.action_validate()
        self.assertEqual(schedule.state, 'validated')

    def test_activate_contract_without_line_error(self):
        contract = self._create_contract(with_line=False)
        with self.assertRaises(UserError):
            contract.action_activate()
        contract_with_line = self._create_contract()
        contract_with_line.action_activate()
        self.assertEqual(contract_with_line.state, 'active')

    def test_invoice_without_validated_interventions_error(self):
        schedule = self._create_schedule()
        line = self._create_line(schedule)
        schedule.action_start()
        schedule.action_submit()
        schedule.action_validate()
        with self.assertRaises(UserError):
            schedule.action_invoice()

    def test_manager_actions_reserved(self):
        site = self._create_site()
        contract = self._create_contract(site=site)
        with self.assertRaises(UserError):
            contract.with_user(self.user).action_activate()
        contract.with_user(self.manager).action_activate()
        self.assertEqual(contract.state, 'active')
        with self.assertRaises(UserError):
            contract.with_user(self.user).action_suspend()
        contract.with_user(self.manager).action_suspend()
        self.assertEqual(contract.state, 'suspended')

    def test_manager_invoice_validation_reserved(self):
        schedule = self._create_schedule()
        line = self._create_line(schedule)
        line.action_mark_done()
        check = self.QualityCheck.create({
            'schedule_line_id': line.id,
            'rating': '4',
        })
        check.action_validate()
        schedule.action_start()
        schedule.action_submit()
        schedule.action_validate()
        with self.assertRaises(UserError):
            schedule.with_user(self.user).action_invoice()
        schedule.with_user(self.manager).action_invoice()
        self.assertEqual(schedule.state, 'invoiced')

    def test_manager_schedule_cancel_reserved(self):
        schedule = self._create_schedule()
        with self.assertRaises(UserError):
            schedule.with_user(self.user).action_cancel()
        schedule.with_user(self.manager).action_cancel()
        self.assertEqual(schedule.state, 'cancelled')

    def test_cron_alert_dedup(self):
        schedule = self._create_schedule(
            planned_date=fields.Date.today() - timedelta(days=10))
        self.env.company.sf_cleaning_overdue_days = 1
        schedule._cron_sf_cleaning_alert()
        schedule._cron_sf_cleaning_alert()
        todo = self.env.ref('mail.mail_activity_data_todo')
        activities = schedule.activity_ids.filtered(
            lambda a: a.activity_type_id == todo)
        self.assertEqual(len(activities), 1)

    def test_cron_alert_unassigned_agent(self):
        schedule = self._create_schedule()
        schedule.agent_id = False
        schedule._cron_sf_cleaning_alert()
        todo = self.env.ref('mail.mail_activity_data_todo')
        activities = schedule.activity_ids.filtered(
            lambda a: a.activity_type_id == todo)
        self.assertEqual(len(activities), 1)
        self.assertEqual(schedule.activity_date, fields.Date.today())

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'Cleaning Company B'})
        site = self.Site.with_company(company_b).create({
            'name': 'Branch Office',
            'partner_id': self.partner.id,
        })
        contract = self.Contract.with_company(company_b).create({
            'partner_id': self.partner.id,
            'billing_period': 'monthly',
        })
        self.ContractLine.create({
            'contract_id': contract.id,
            'site_id': site.id,
        })
        schedule = self.Schedule.with_company(company_b).create({
            'contract_id': contract.id,
            'site_id': site.id,
            'planned_date': fields.Date.today(),
        })
        found = self.Schedule.with_user(self.user).search(
            [('id', '=', schedule.id)])
        self.assertNotIn(schedule, found)
        found_manager = self.Schedule.with_user(self.manager).search(
            [('id', '=', schedule.id)])
        self.assertIn(schedule, found_manager)

    def test_reports_render(self):
        site = self._create_site()
        contract = self._create_contract(site=site)
        schedule = self._create_schedule(contract=contract, site=site)
        line = self._create_line(schedule)
        line.action_mark_done()
        check = self.QualityCheck.create({
            'schedule_line_id': line.id,
            'rating': '5',
        })
        check.action_validate()
        schedule.action_start()
        schedule.action_submit()
        schedule.action_validate()
        mission_report = self.env.ref(
            'sf_cleaning.report_sf_cleaning_mission')
        result = mission_report._render_qweb_html(schedule.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Order of Mission', html)
        summary_report = self.env.ref(
            'sf_cleaning.report_sf_cleaning_monthly_summary')
        result = summary_report._render_qweb_html(contract.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Monthly Service Summary', html)