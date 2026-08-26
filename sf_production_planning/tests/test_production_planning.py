# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductionPlanning(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Mps = self.env['sf.mps']
        self.Line = self.env['sf.mps.line']
        self.group_user = self.env.ref(
            'sf_production_planning.group_production_user')
        self.workcenter = self.env['mrp.workcenter'].create({
            'name': 'Machine A',
            'time_efficiency': 0.5,
        })
        self.product = self.env['product.product'].create({
            'name': 'Widget',
            'type': 'product',
        })

    def _create_plan(self, state='draft'):
        return self.Mps.create({
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + timedelta(days=30),
            'state': state,
        })

    def _create_line(self, plan, state='planned', priority='normal',
                     quantity=10.0):
        return self.Line.create({
            'mps_id': plan.id,
            'workcenter_id': self.workcenter.id,
            'product_id': self.product.id,
            'quantity': quantity,
            'date_start': fields.Datetime.now(),
            'date_end': fields.Datetime.now() + timedelta(hours=5),
            'priority': priority,
            'state': state,
        })

    def test_create_plan_with_sequence(self):
        plan = self._create_plan()
        self.assertTrue(plan.name.startswith('MPS-'))

    def test_create_line_planned(self):
        plan = self._create_plan()
        line = self._create_line(plan)
        self.assertEqual(line.state, 'planned')
        self.assertEqual(line.company_id, plan.company_id)

    def test_confirm_plan(self):
        plan = self._create_plan()
        plan.action_confirm()
        self.assertEqual(plan.state, 'confirmed')

    def test_close_requires_confirmed(self):
        plan = self._create_plan()
        with self.assertRaises(UserError):
            plan.action_close()

    def test_delete_confirmed_plan(self):
        plan = self._create_plan()
        plan.action_confirm()
        with self.assertRaises(UserError):
            plan.unlink()

    def test_delete_confirmed_line(self):
        plan = self._create_plan()
        line = self._create_line(plan, state='confirmed')
        with self.assertRaises(UserError):
            line.unlink()

    def test_load_productions(self):
        plan = self._create_plan()
        production = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 20.0,
            'state': 'draft',
        })
        wizard = self.env['sf.mps.load.wizard'].create({
            'mps_id': plan.id,
            'workcenter_id': self.workcenter.id,
            'production_ids': [(6, 0, production.ids)],
        })
        wizard.action_load()
        line = self.Line.search([('mps_id', '=', plan.id)])
        self.assertEqual(len(line), 1)
        self.assertEqual(line.production_id, production)
        self.assertEqual(line.product_id, self.product)
        self.assertEqual(line.quantity, 20.0)
        self.assertTrue(line.date_end >= line.date_start)

    def test_workcenter_load(self):
        plan = self._create_plan()
        self._create_line(plan, quantity=4.0)
        self._create_line(plan, quantity=6.0)
        lines = self.Line.search([('mps_id', '=', plan.id)])
        load = plan._check_workcenter_load()
        self.assertAlmostEqual(load[self.workcenter], 5.0)

    def test_line_set_done(self):
        plan = self._create_plan()
        line = self._create_line(plan, state='confirmed')
        line.action_set_done()
        self.assertEqual(line.state, 'done')

    def test_set_done_requires_confirmed(self):
        plan = self._create_plan()
        line = self._create_line(plan)
        with self.assertRaises(UserError):
            line.action_set_done()

    def test_date_constraint(self):
        plan = self._create_plan()
        with self.assertRaises(ValidationError):
            self.Mps.create({
                'date_start': fields.Date.today() + timedelta(days=10),
                'date_end': fields.Date.today(),
            })

    def test_multi_company_rule(self):
        plan = self._create_plan()
        company_b = self.env['res.company'].create({'name': 'MPS Company B'})
        user = self.env['res.users'].create({
            'name': 'MPS Company A User',
            'login': 'mps_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Mps.with_company(company_b).create({
            'date_start': fields.Date.today(),
            'date_end': fields.Date.today() + timedelta(days=30),
        })
        self.assertNotIn(other, self.Mps.with_user(user).search(
            [('id', '=', other.id)]))