# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestApprovalEngine(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = cls.env.ref('base.user_admin')
        cls.user = cls.env['res.users'].create({
            'name': 'Approval User',
            'login': 'approval_user_test',
            'groups_id': [(6, 0, [
                cls.env.ref('base.group_user').id,
                cls.env.ref('sf_approval_engine.group_approval_user').id,
            ])],
        })
        cls.manager = cls.env['res.users'].create({
            'name': 'Approval Manager',
            'login': 'approval_manager_test',
            'groups_id': [(6, 0, [
                cls.env.ref('base.group_user').id,
                cls.env.ref('sf_approval_engine.group_approval_manager').id,
            ])],
        })
        cls.model_purchase = cls.env.ref('base.model_purchase_order')
        cls.product = cls.env['product.product'].create({
            'name': 'Approval Product',
            'type': 'consu',
            'list_price': 50.0,
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Approval Vendor',
        })

    def _new_template(self, steps=None):
        template = self.env['sf.approval.template'].create({
            'name': 'Purchase Approval',
            'model_id': self.model_purchase.id,
        })
        if steps:
            template.write({'step_ids': [(0, 0, vals) for vals in steps]})
        return template

    def _new_request(self, template, amount=100.0):
        return self.env['sf.approval.request'].create({
            'name': 'APR-TEST',
            'template_id': template.id,
            'requester_id': self.user.id,
            'amount': amount,
            'document_name': 'PO00001',
            'state': 'draft',
        })

    def test_01_template_steps_required(self):
        template = self._new_template()
        self.assertTrue(template.name)
        self.assertEqual(template.model_id.id, self.model_purchase.id)

    def test_02_duplicate_sequence_rejected(self):
        with self.assertRaises(ValidationError):
            self._new_template([
                {'sequence': 1, 'name': 'First', 'assignment': 'specific',
                 'user_id': self.admin.id},
                {'sequence': 1, 'name': 'Second', 'assignment': 'specific',
                 'user_id': self.admin.id},
            ])

    def test_03_submit_single_step(self):
        template = self._new_template([
            {'sequence': 1, 'name': 'Manager OK', 'assignment': 'specific',
             'user_id': self.manager.id},
        ])
        request = self._new_request(template)
        request.action_submit()
        self.assertEqual(request.state, 'submitted')
        self.assertEqual(request.current_step_id.sequence, 1)
        self.assertIn(self.manager, request.approver_ids)

    def test_04_approve_single_step(self):
        template = self._new_template([
            {'sequence': 1, 'name': 'Manager OK', 'assignment': 'specific',
             'user_id': self.manager.id},
        ])
        request = self._new_request(template)
        request.action_submit()
        request.with_user(self.manager).action_approve()
        self.assertEqual(request.state, 'approved')
        self.assertEqual(len(request.step_history_ids), 1)
        self.assertEqual(request.step_history_ids.action, 'approved')

    def test_05_multi_step_flow(self):
        template = self._new_template([
            {'sequence': 1, 'name': 'Team Lead', 'assignment': 'specific',
             'user_id': self.user.id},
            {'sequence': 2, 'name': 'Manager', 'assignment': 'specific',
             'user_id': self.manager.id},
        ])
        request = self._new_request(template)
        request.action_submit()
        self.assertEqual(request.current_step_id.sequence, 1)
        request.with_user(self.user).action_approve()
        self.assertEqual(request.current_step_id.sequence, 2)
        self.assertEqual(request.state, 'submitted')
        request.with_user(self.manager).action_approve()
        self.assertEqual(request.state, 'approved')

    def test_06_reject(self):
        template = self._new_template([
            {'sequence': 1, 'name': 'Manager OK', 'assignment': 'specific',
             'user_id': self.manager.id},
        ])
        request = self._new_request(template)
        request.action_submit()
        request.with_user(self.manager).action_reject('Too expensive')
        self.assertEqual(request.state, 'rejected')
        self.assertEqual(request.rejected_reason, 'Too expensive')
        request.action_draft()
        self.assertEqual(request.state, 'draft')

    def test_07_non_approver_cannot_approve(self):
        template = self._new_template([
            {'sequence': 1, 'name': 'Manager OK', 'assignment': 'specific',
             'user_id': self.manager.id},
        ])
        request = self._new_request(template)
        request.action_submit()
        with self.assertRaises(ValidationError):
            request.with_user(self.user).action_approve()

    def test_08_amount_threshold_skip(self):
        template = self._new_template([
            {'sequence': 1, 'name': 'High value', 'assignment': 'specific',
             'user_id': self.manager.id, 'min_amount': 1000.0},
        ])
        low = self._new_request(template, amount=100.0)
        low.action_submit()
        self.assertEqual(low.state, 'approved')