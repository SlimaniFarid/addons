# -*- coding: utf-8 -*-
import uuid

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfAqlSampling(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Product %s' % uuid.uuid4().hex[:6],
        })
        self.supplier = self.env['res.partner'].create({
            'name': 'Supplier %s' % uuid.uuid4().hex[:6],
        })
        self.plan = self.env['sf.aql.plan'].create({
            'inspection_level': 'II',
            'lot_size_min': 0,
            'lot_size_max': 100,
            'sample_size': 10,
            'accept_number': 1,
            'reject_number': 2,
        })
        self.plan_big = self.env['sf.aql.plan'].create({
            'inspection_level': 'II',
            'lot_size_min': 101,
            'lot_size_max': 1000,
            'sample_size': 20,
            'accept_number': 2,
            'reject_number': 3,
        })
        self.manager_group = self.env.ref(
            'sf_aql_sampling.group_sf_aql_sampling_manager')
        self.user_group = self.env.ref(
            'sf_aql_sampling.group_sf_aql_sampling_user')
        self.manager = self.env['res.users'].create({
            'name': 'AQL Manager',
            'login': 'aql_mgr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.manager_group.id])],
        })

    def _create_inspection(self, lot_quantity=50.0, **kw):
        vals = {
            'product_id': self.product.id,
            'partner_id': self.supplier.id,
            'source': 'incoming',
            'lot_quantity': lot_quantity,
        }
        vals.update(kw)
        return self.env['sf.aql.inspection'].create(vals)

    def _add_defect(self, inspection, severity='minor', quantity=1):
        return self.env['sf.aql.defect'].create({
            'inspection_id': inspection.id,
            'severity': severity,
            'quantity': quantity,
            'description': 'Test defect',
        })

    def test_sequences(self):
        plan = self.env['sf.aql.plan'].create({
            'inspection_level': 'II',
            'lot_size_min': 0,
            'lot_size_max': 50,
            'sample_size': 5,
            'accept_number': 0,
            'reject_number': 1,
        })
        self.assertTrue(plan.name.startswith('AQL-'))
        inspection = self._create_inspection()
        self.assertTrue(inspection.name.startswith('INS-'))

    def test_plan_selection(self):
        inspection = self._create_inspection(lot_quantity=50.0)
        self.assertEqual(inspection.plan_id, self.plan)
        self.assertEqual(inspection.sample_size, 10)
        big = self._create_inspection(lot_quantity=500.0)
        self.assertEqual(big.plan_id, self.plan_big)
        self.assertEqual(big.sample_size, 20)

    def test_decision_accepted(self):
        inspection = self._create_inspection()
        inspection.action_start()
        self._add_defect(inspection, 'minor', 1)
        self.assertEqual(inspection.weighted_defects, 1)
        self.assertEqual(inspection.decision, 'accepted')

    def test_decision_rejected_weight(self):
        inspection = self._create_inspection()
        inspection.action_start()
        self._add_defect(inspection, 'major', 1)
        self.assertEqual(inspection.weighted_defects, 5)
        self.assertEqual(inspection.decision, 'rejected')

    def test_decision_rejected_critical(self):
        inspection = self._create_inspection()
        inspection.action_start()
        self._add_defect(inspection, 'critical', 1)
        self.assertEqual(inspection.critical_defects, 1)
        self.assertEqual(inspection.decision, 'rejected')

    def test_workflow_release(self):
        inspection = self._create_inspection()
        inspection.action_start()
        self._add_defect(inspection, 'minor', 1)
        inspection.action_complete()
        self.assertEqual(inspection.state, 'completed')
        inspection.with_user(self.manager).action_release()
        self.assertEqual(inspection.state, 'released')

    def test_user_cannot_release(self):
        inspection = self._create_inspection()
        inspection.action_start()
        inspection.action_complete()
        with self.assertRaises(UserError):
            inspection.action_release()

    def test_reject_requires_rejected_decision(self):
        inspection = self._create_inspection()
        inspection.action_start()
        self._add_defect(inspection, 'minor', 1)
        inspection.action_complete()
        with self.assertRaises(UserError):
            inspection.with_user(self.manager).action_reject()
        inspection2 = self._create_inspection()
        inspection2.action_start()
        self._add_defect(inspection2, 'critical', 1)
        inspection2.action_complete()
        inspection2.with_user(self.manager).action_reject()
        self.assertEqual(inspection2.state, 'rejected')

    def test_plan_constraints(self):
        with self.assertRaises(ValidationError):
            self.env['sf.aql.plan'].create({
                'inspection_level': 'II',
                'lot_size_min': 50,
                'lot_size_max': 10,
                'sample_size': 5,
                'accept_number': 0,
                'reject_number': 1,
            })
        with self.assertRaises(ValidationError):
            self.env['sf.aql.plan'].create({
                'inspection_level': 'II',
                'lot_size_min': 0,
                'lot_size_max': 10,
                'sample_size': 5,
                'accept_number': 2,
                'reject_number': 2,
            })

    def test_defect_quantity_positive(self):
        inspection = self._create_inspection()
        with self.assertRaises(ValidationError):
            self.env['sf.aql.defect'].create({
                'inspection_id': inspection.id,
                'severity': 'minor',
                'quantity': 0,
            })

    def test_defect_not_editable_after_release(self):
        inspection = self._create_inspection()
        inspection.action_start()
        defect = self._add_defect(inspection, 'minor', 1)
        inspection.action_complete()
        inspection.with_user(self.manager).action_release()
        with self.assertRaises(UserError):
            defect.quantity = 3

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'AQL Co 2'})
        inspection2 = self.env['sf.aql.inspection'].with_company(company2).create({
            'product_id': self.product.id,
            'source': 'incoming',
            'lot_quantity': 10.0,
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'AQL User',
            'login': 'aql_usr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.user_group.id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.aql.inspection'].with_user(user).search(
            [('id', '=', inspection2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        inspection = self._create_inspection()
        inspection.action_start()
        self._add_defect(inspection, 'minor', 1)
        action = self.env.ref(
            'sf_aql_sampling.action_report_aql_inspection').report_action(inspection)
        self.assertTrue(action)