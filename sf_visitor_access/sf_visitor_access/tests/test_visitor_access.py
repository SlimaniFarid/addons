# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestVisitorAccess(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Visit = self.env['sf.visitor.visit']
        self.Gate = self.env['sf.visitor.gate']
        self.group_user = self.env.ref('sf_visitor_access.group_visitor_user')

    def _create_gate(self, with_rule=False):
        gate = self.Gate.create({'name': 'Main Site', 'site_code': 'SITE-1'})
        if with_rule:
            self.env['sf.visitor.rule'].create({
                'gate_id': gate.id,
                'version': 1,
                'name': 'Safety Rules v1',
                'body': '<p>Wear PPE</p>',
            })
        return gate

    def _create_visit(self, gate=None, state='draft'):
        return self.Visit.create({
            'gate_id': (gate or self._create_gate()).id,
            'visit_type': 'visitor',
            'full_name': 'John Doe',
            'state': state,
        })

    def test_create_visit_with_sequence(self):
        visit = self._create_visit()
        self.assertTrue(visit.name.startswith('VIS-'))

    def test_check_in_without_rules(self):
        visit = self._create_visit()
        visit.action_check_in()
        self.assertEqual(visit.state, 'checked_in')
        self.assertTrue(visit.badge_number)
        self.assertTrue(visit.check_in)

    def test_check_in_requires_safety_acceptance(self):
        gate = self._create_gate(with_rule=True)
        visit = self._create_visit(gate=gate)
        with self.assertRaises(UserError):
            visit.action_check_in()

    def test_check_in_with_safety_acceptance(self):
        gate = self._create_gate(with_rule=True)
        visit = self._create_visit(gate=gate)
        visit.safety_rule_ok = True
        visit.action_check_in()
        self.assertEqual(visit.state, 'checked_in')
        self.assertEqual(visit.rule_version, 1)

    def test_check_out_and_archive(self):
        visit = self._create_visit()
        visit.action_check_in()
        visit.action_check_out()
        self.assertEqual(visit.state, 'checked_out')
        self.assertTrue(visit.check_out)
        visit.action_archive()
        self.assertEqual(visit.state, 'archived')
        self.assertFalse(visit.active)

    def test_check_out_non_checked_in(self):
        visit = self._create_visit()
        with self.assertRaises(UserError):
            visit.action_check_out()

    def test_present_on_site_list(self):
        visit = self._create_visit()
        visit.action_check_in()
        present = self.Visit.search([('state', '=', 'checked_in')])
        self.assertIn(visit, present)

    def test_no_show(self):
        visit = self._create_visit()
        visit.action_no_show()
        self.assertEqual(visit.state, 'no_show')

    def test_unique_badge(self):
        first = self._create_visit()
        first.action_check_in()
        with self.assertRaises(Exception):
            self.Visit.create({
                'gate_id': first.gate_id.id,
                'visit_type': 'visitor',
                'full_name': 'Second Visitor',
                'badge_number': first.badge_number,
            })

    def test_check_in_cannot_be_deleted(self):
        visit = self._create_visit()
        visit.action_check_in()
        with self.assertRaises(UserError):
            visit.unlink()

    def test_checkout_before_checkin(self):
        visit = self._create_visit()
        visit.write({'check_in': fields.Datetime.now()})
        with self.assertRaises(ValidationError):
            visit.write({'check_out': fields.Datetime.now()
                         - timedelta(hours=2)})

    def test_overtime_alert(self):
        visit = self._create_visit()
        visit.action_check_in()
        visit.write({'check_in': fields.Datetime.now() - timedelta(hours=10)})
        self.env.company.sf_visitor_alert_hours = 1
        visit._check_visitor_overtime()
        self.assertTrue(visit.activity_ids)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Visitor Company B'})
        user = self.env['res.users'].create({
            'name': 'Visitor Company A User',
            'login': 'visitor_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        gate = self._create_gate()
        other = self.Visit.with_company(company_b).create({
            'gate_id': gate.id,
            'visit_type': 'visitor',
            'full_name': 'Jane Doe',
        })
        self.assertNotIn(other, self.Visit.with_user(user).search(
            [('id', '=', other.id)]))