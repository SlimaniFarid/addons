# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHaccp(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Site = self.env['sf.haccp.site']
        self.Plan = self.env['sf.haccp.plan']
        self.Step = self.env['sf.haccp.step']
        self.Prerequisite = self.env['sf.haccp.prerequisite']
        self.Check = self.env['sf.haccp.check']
        self.Nonconformity = self.env['sf.haccp.nonconformity']
        self.group_user = self.env.ref('sf_haccp.group_haccp_user')
        self.env.user.groups_id |= self.env.ref(
            'sf_haccp.group_haccp_manager')

    def _create_site(self, name='Central Kitchen'):
        return self.Site.create({'name': name, 'address': '1 Food Street'})

    def _create_plan(self, site=None):
        return self.Plan.create({
            'site_id': (site or self._create_site()).id,
            'process': 'Cold storage',
        })

    def _create_check(self, site=None, plan=None, result=False,
                      target_min=0.0, target_max=4.0):
        return self.Check.create({
            'site_id': (site or self._create_site()).id,
            'plan_id': (plan or self._create_plan()).id,
            'check_type': 'temperature',
            'target_min': target_min,
            'target_max': target_max,
            'unit': 'C',
            'result': result,
            'control_date': fields.Datetime.now(),
        })

    def _create_user(self, name='HACCP User', login='haccp_user',
                     group=None):
        return self.env['res.users'].create({
            'name': name,
            'login': login,
            'groups_id': [(4, (group or self.group_user).id)],
        })

    def test_create_records_with_sequences(self):
        site = self._create_site()
        plan = self._create_plan(site)
        self.Step.create({
            'plan_id': plan.id,
            'name': 'Receive goods',
            'hazard': 'Biological',
            'is_ccp': True,
            'critical_limit': '0-4 C',
        })
        prerequisite = self.Prerequisite.create({
            'site_id': site.id,
            'category': 'cleaning',
            'description': 'Daily cleaning schedule',
        })
        check = self._create_check(site, plan)
        nc = self.Nonconformity.create({
            'site_id': site.id,
            'description': 'Cold storage breach',
            'severity': 'major',
        })
        self.assertTrue(site.name.startswith('SIT-'))
        self.assertTrue(plan.name.startswith('PLN-'))
        self.assertTrue(prerequisite.name.startswith('PRE-'))
        self.assertTrue(check.name.startswith('CHK-'))
        self.assertTrue(nc.name.startswith('NCN-'))

    def test_automatic_deviation_detection(self):
        check = self._create_check(result=9.0)
        check.action_validate()
        self.assertEqual(check.state, 'deviated')
        self.assertTrue(check.deviation_detail)
        nc = self.Nonconformity.search([('check_id', '=', check.id)])
        self.assertTrue(nc)
        self.assertEqual(nc.state, 'open')

    def test_no_deviation_when_within_range(self):
        check = self._create_check(result=3.0)
        check.action_validate()
        self.assertEqual(check.state, 'done')
        self.assertFalse(self.Nonconformity.search(
            [('check_id', '=', check.id)]))

    def test_validate_requires_result(self):
        check = self._create_check()
        with self.assertRaises(UserError):
            check.action_validate()
        self.assertEqual(check.state, 'scheduled')

    def test_nc_closure_requires_manager_and_corrective_action(self):
        check = self._create_check(result=9.0)
        check.action_validate()
        nc = self.Nonconformity.search([('check_id', '=', check.id)])
        user = self._create_user()
        nc.write({
            'corrective_action': 'Reset the cold room and requalify.',
            'due_date': fields.Date.today() + timedelta(days=5),
        })
        with self.assertRaises(UserError):
            nc.with_user(user).action_close()
        self.assertEqual(nc.state, 'open')
        nc.action_close()
        self.assertEqual(nc.state, 'closed')
        self.assertTrue(nc.closed_date)
        self.assertEqual(check.state, 'resolved')

    def test_nc_close_requires_corrective_action(self):
        check = self._create_check(result=9.0)
        check.action_validate()
        nc = self.Nonconformity.search([('check_id', '=', check.id)])
        nc.write({'due_date': fields.Date.today() + timedelta(days=5)})
        with self.assertRaises(UserError):
            nc.action_close()
        self.assertEqual(nc.state, 'open')

    def test_cron_creates_activities(self):
        check = self.Check.create({
            'site_id': self._create_site().id,
            'check_type': 'temperature',
            'control_date': fields.Datetime.now() - timedelta(days=2),
        })
        nc = self.Nonconformity.create({
            'site_id': check.site_id.id,
            'description': 'Overdue corrective action',
            'state': 'open',
            'due_date': fields.Date.today() - timedelta(days=1),
        })
        self.env.company.sf_haccp_alert_days = 0
        check._check_haccp_controls()
        self.assertTrue(check.activity_ids)
        self.assertTrue(nc.activity_ids)
        count_before = len(check.activity_ids) + len(nc.activity_ids)
        check._check_haccp_controls()
        self.assertEqual(len(check.activity_ids) + len(nc.activity_ids),
                         count_before)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'HACCP Company B'})
        user = self._create_user(name='HACCP Company A User',
                                 login='haccp_company_a_user')
        site = self.Site.with_company(company_b).create({'name': 'Site B'})
        self.assertNotIn(site, self.Site.with_user(user).search(
            [('id', '=', site.id)]))

    def test_report_records_exist(self):
        reports = self.env['ir.actions.report'].search([
            ('report_name', 'in', [
                'sf_haccp.report_haccp_register_template',
                'sf_haccp.report_nonconformities_template',
            ])])
        self.assertEqual(len(reports), 2)