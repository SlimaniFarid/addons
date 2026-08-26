# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestPsa(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Engagement = self.env['sf.psa.engagement']
        self.Resource = self.env['sf.psa.resource']
        self.Assignment = self.env['sf.psa.assignment']
        self.TimeEntry = self.env['sf.psa.time.entry']
        self.partner = self.env['res.partner'].create({'name': 'ACME Corp'})
        self.consultant = self.env['res.partner'].create({
            'name': 'John Doe'})
        self.resource = self.Resource.create({
            'partner_id': self.consultant.id,
            'role': 'Consultant',
            'hourly_rate': 100.0,
            'capacity_hours': 40.0,
        })
        self.engagement = self.Engagement.create({
            'name': 'ERP Implementation',
            'code': 'ENG-001',
            'partner_id': self.partner.id,
            'budget_hours': 100.0,
        })

    def test_01_engagement_creation(self):
        self.assertEqual(self.engagement.code, 'ENG-001')
        self.assertEqual(self.engagement.state, 'draft')
        self.assertEqual(self.engagement.logged_hours, 0.0)

    def test_02_engagement_code_unique(self):
        with self.assertRaises(Exception):
            self.Engagement.create({
                'name': 'Other', 'code': 'ENG-001',
                'partner_id': self.partner.id})

    def test_03_state_flow(self):
        self.engagement.action_start()
        self.assertEqual(self.engagement.state, 'active')
        self.engagement.action_close()
        self.assertEqual(self.engagement.state, 'closed')

    def test_04_assignment_creation(self):
        assign = self.Assignment.create({
            'engagement_id': self.engagement.id,
            'resource_id': self.resource.id,
            'allocated_hours': 80.0,
        })
        self.assertEqual(assign.logged_hours, 0.0)
        self.assertEqual(assign.utilization, 0.0)

    def test_05_time_entry_amount(self):
        assign = self.Assignment.create({
            'engagement_id': self.engagement.id,
            'resource_id': self.resource.id,
            'allocated_hours': 80.0,
        })
        entry = self.TimeEntry.create({
            'engagement_id': self.engagement.id,
            'assignment_id': assign.id,
            'resource_id': self.resource.id,
            'hours': 10.0,
            'billable': True,
        })
        self.assertEqual(entry.amount, 1000.0)
        self.assertEqual(assign.logged_hours, 10.0)
        self.assertEqual(self.engagement.logged_hours, 10.0)
        self.assertEqual(assign.utilization, 12.5)

    def test_06_non_billable_amount_zero(self):
        assign = self.Assignment.create({
            'engagement_id': self.engagement.id,
            'resource_id': self.resource.id,
        })
        entry = self.TimeEntry.create({
            'engagement_id': self.engagement.id,
            'assignment_id': assign.id,
            'resource_id': self.resource.id,
            'hours': 5.0,
            'billable': False,
        })
        self.assertEqual(entry.amount, 0.0)

    def test_07_progress_capped(self):
        assign = self.Assignment.create({
            'engagement_id': self.engagement.id,
            'resource_id': self.resource.id,
        })
        self.TimeEntry.create({
            'engagement_id': self.engagement.id,
            'assignment_id': assign.id,
            'resource_id': self.resource.id,
            'hours': 300.0,
        })
        self.assertEqual(self.engagement.progress, 100.0)