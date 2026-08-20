# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, timedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfBatchRecords(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Product %s' % uuid.uuid4().hex[:6],
        })
        self.operator = self.env.user
        self.manager_group = self.env.ref(
            'sf_batch_records.group_sf_batch_records_manager')
        self.user_group = self.env.ref(
            'sf_batch_records.group_sf_batch_records_user')
        self.manager = self.env['res.users'].create({
            'name': 'Batch Manager',
            'login': 'batch_mgr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.manager_group.id])],
        })

    def _create_record(self, **kw):
        vals = {
            'product_id': self.product.id,
            'quantity': 100.0,
            'uom_name': 'kg',
        }
        vals.update(kw)
        return self.env['sf.batch.record'].create(vals)

    def _add_parameter(self, record, actual=20.0, min_value=15.0,
                       max_value=25.0, **kw):
        vals = {
            'batch_record_id': record.id,
            'step_id': record.step_ids[:1].id or False,
            'name': 'Temperature',
            'unit': 'C',
            'min_value': min_value,
            'max_value': max_value,
            'actual_value': actual,
        }
        vals.update(kw)
        return self.env['sf.batch.record.parameter'].create(vals)

    def test_sequence(self):
        record = self._create_record()
        self.assertTrue(record.name.startswith('BPR-'))

    def test_workflow(self):
        record = self._create_record()
        record.action_start()
        self.assertEqual(record.state, 'in_progress')
        record.action_submit_review()
        self.assertEqual(record.state, 'under_review')
        record.with_user(self.manager).action_release()
        self.assertEqual(record.state, 'released')
        self.assertTrue(record.released_by)

    def test_reject(self):
        record = self._create_record()
        record.action_submit_review()
        record.with_user(self.manager).action_reject()
        self.assertEqual(record.state, 'rejected')

    def test_user_cannot_release(self):
        record = self._create_record()
        record.action_submit_review()
        with self.assertRaises(UserError):
            record.action_release()

    def test_parameter_status(self):
        record = self._create_record()
        record.action_start()
        param = self._add_parameter(record, actual=30.0)
        self.assertEqual(param.status, 'out_of_spec')
        param.actual_value = 20.0
        self.assertEqual(param.status, 'in_spec')

    def test_release_blocked_without_deviation(self):
        record = self._create_record()
        record.action_start()
        self._add_parameter(record, actual=30.0)
        record.action_submit_review()
        self.assertEqual(record.out_of_spec_params, 1)
        with self.assertRaises(UserError):
            record.with_user(self.manager).action_release()

    def test_release_with_approved_deviation(self):
        record = self._create_record()
        record.action_start()
        param = self._add_parameter(record, actual=30.0)
        deviation = self.env['sf.batch.record.deviation'].create({
            'batch_record_id': record.id,
            'description': 'High temperature during mixing',
            'category': 'parameter',
            'severity': 'major',
            'parameter_id': param.id,
            'corrective_action': 'Extended cooling time',
        })
        self.assertEqual(record.out_of_spec_params, 1)
        deviation.with_user(self.manager).action_approve()
        self.assertEqual(deviation.state, 'approved')
        self.assertEqual(record.out_of_spec_params, 0)
        record.action_submit_review()
        record.with_user(self.manager).action_release()
        self.assertEqual(record.state, 'released')

    def test_user_cannot_approve_deviation(self):
        record = self._create_record()
        deviation = self.env['sf.batch.record.deviation'].create({
            'batch_record_id': record.id,
            'description': 'Test deviation',
        })
        with self.assertRaises(UserError):
            deviation.action_approve()

    def test_parameter_not_editable_under_review(self):
        record = self._create_record()
        record.action_start()
        param = self._add_parameter(record, actual=20.0)
        record.action_submit_review()
        with self.assertRaises(UserError):
            param.actual_value = 30.0

    def test_material_quantity_positive(self):
        record = self._create_record()
        with self.assertRaises(ValidationError):
            self.env['sf.batch.record.material'].create({
                'batch_record_id': record.id,
                'product_id': self.product.id,
                'quantity': 0.0,
            })

    def test_step_end_before_start_blocked(self):
        record = self._create_record()
        step = self.env['sf.batch.record.step'].create({
            'batch_record_id': record.id,
            'step_name': 'Mixing',
            'operator_id': self.operator.id,
        })
        now = datetime.now()
        with self.assertRaises(ValidationError):
            step.write({
                'started_at': now,
                'ended_at': now - timedelta(hours=1),
            })

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Batch Co 2'})
        record2 = self.env['sf.batch.record'].with_company(company2).create({
            'product_id': self.product.id,
            'quantity': 1.0,
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'Batch User',
            'login': 'batch_usr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.user_group.id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.batch.record'].with_user(user).search(
            [('id', '=', record2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        record = self._create_record()
        record.action_start()
        self._add_parameter(record, actual=20.0)
        action = self.env.ref(
            'sf_batch_records.action_report_batch_record').report_action(record)
        self.assertTrue(action)