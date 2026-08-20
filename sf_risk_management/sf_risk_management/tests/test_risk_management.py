# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields


class TestRisk(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Risk = self.env['sf.risk']
        self.Action = self.env['sf.risk.action']
        self.Control = self.env['sf.risk.control']
        self.Test = self.env['sf.risk.control.test']
        self.Requirement = self.env['sf.risk.requirement']
        self.owner = self.env['res.users'].create({
            'name': 'Owner',
            'login': 'risk_owner_test',
        })
        self.manager = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'risk_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_risk_management.group_risk_manager').id,
                ]),
            ],
        })
        self.user = self.env['res.users'].create({
            'name': 'User',
            'login': 'risk_user_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_risk_management.group_risk_user').id,
                ]),
            ],
        })

    def _make_risk(self, **kw):
        vals = {
            'name': 'Data breach',
            'category': 'cyber',
            'description': 'Risk of customer data breach',
            'probability': 4,
            'impact': 5,
            'risk_owner_id': self.owner.id,
        }
        vals.update(kw)
        return self.Risk.create(vals)

    def test_01_risk_score_and_class(self):
        risk = self._make_risk()
        self.assertEqual(risk.risk_score, 20)
        self.assertEqual(risk.risk_class, 'extreme')

    def test_02_workflow_to_monitored(self):
        risk = self._make_risk()
        risk.action_assess()
        self.assertEqual(risk.state, 'assessed')
        self.Action.create({
            'risk_id': risk.id,
            'name': 'Encrypt data',
            'responsible_id': self.owner.id,
            'due_date': fields.Date.today(),
        })
        risk.action_plan_treatment()
        self.assertEqual(risk.state, 'treatment_planned')
        risk.actions.action_start()
        risk.actions.evidence = 'Encryption deployed'
        risk.actions.action_done()
        risk.action_monitor()
        self.assertEqual(risk.state, 'monitored')

    def test_03_monitor_requires_plan(self):
        risk = self._make_risk()
        risk.action_assess()
        risk.action_plan_treatment()
        with self.assertRaises(UserError):
            risk.action_monitor()

    def test_04_high_risk_requires_owner(self):
        risk = self._make_risk(risk_owner_id=False)
        with self.assertRaises(UserError):
            risk.action_assess()

    def test_05_failed_test_requires_action(self):
        control = self.Control.create({
            'name': 'Access review',
        })
        with self.assertRaises(UserError):
            self.Test.create({
                'control_id': control.id,
                'result': 'failed',
            })

    def test_06_control_last_test(self):
        control = self.Control.create({
            'name': 'Access review',
        })
        action = self.Action.create({
            'risk_id': self._make_risk().id,
            'name': 'Fix access',
            'responsible_id': self.owner.id,
            'due_date': fields.Date.today(),
        })
        self.assertEqual(control.last_test_result, 'not_tested')
        self.Test.create({
            'control_id': control.id,
            'result': 'passed',
        })
        self.assertEqual(control.last_test_result, 'passed')
        self.Test.create({
            'control_id': control.id,
            'result': 'failed',
            'action_id': action.id,
        })
        self.assertEqual(control.last_test_result, 'failed')

    def test_07_requirement_link_unique(self):
        req = self.Requirement.create({
            'name': 'NIS2 risk management',
            'code': 'NIS2-Art21',
            'regulation': 'nis2',
        })
        risk = self._make_risk()
        Link = self.env['sf.risk.requirement.link']
        Link.create({
            'requirement_id': req.id,
            'risk_id': risk.id,
        })
        with self.assertRaises(Exception):
            Link.create({
                'requirement_id': req.id,
                'risk_id': risk.id,
            })
        links = Link.search([
            ('requirement_id', '=', req.id),
            ('risk_id', '=', risk.id),
        ])
        self.assertEqual(len(links), 1)

    def test_08_matrix_out_of_bounds(self):
        with self.assertRaises(UserError):
            self._make_risk(probability=6, impact=2)

    def test_09_active_risk_not_deletable(self):
        risk = self._make_risk()
        with self.assertRaises(UserError):
            risk.unlink()

    def test_10_action_done_requires_evidence(self):
        risk = self._make_risk()
        action = self.Action.create({
            'risk_id': risk.id,
            'name': 'Encrypt data',
            'responsible_id': self.owner.id,
            'due_date': fields.Date.today(),
        })
        action.action_start()
        with self.assertRaises(UserError):
            action.action_done()
        action.evidence = 'Done'
        action.action_done()
        self.assertEqual(action.state, 'done')