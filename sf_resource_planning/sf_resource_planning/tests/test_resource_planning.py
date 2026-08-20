# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestResourcePlanning(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Resource = self.env['sf.resource.planning.resource']
        self.Allocation = self.env['sf.resource.planning.allocation']
        self.resource = self.Resource.create({
            'name': 'John Engineer',
            'resource_type': 'human',
            'capacity_per_day': 8.0,
        })

    def test_01_resource_creation(self):
        self.assertEqual(self.resource.resource_type, 'human')
        self.assertEqual(self.resource.capacity_per_day, 8.0)
        self.assertEqual(self.resource.utilization, 0.0)

    def test_02_allocation_load(self):
        self.Allocation.create({
            'resource_id': self.resource.id,
            'date_start': '2026-08-01',
            'hours': 4.0,
        })
        self.Allocation.create({
            'resource_id': self.resource.id,
            'date_start': '2026-08-02',
            'hours': 4.0,
        })
        self.assertEqual(self.resource.total_allocated, 8.0)
        self.assertEqual(self.resource.utilization, 100.0)

    def test_03_overload(self):
        self.Allocation.create({
            'resource_id': self.resource.id,
            'date_start': '2026-08-01',
            'hours': 12.0,
        })
        self.assertGreater(self.resource.utilization, 100.0)

    def test_04_hours_must_be_positive(self):
        with self.assertRaises(ValidationError):
            self.Allocation.create({
                'resource_id': self.resource.id,
                'date_start': '2026-08-01',
                'hours': -3.0,
            })

    def test_05_machine_resource(self):
        machine = self.Resource.create({
            'name': 'CNC Machine',
            'resource_type': 'machine',
            'capacity_per_day': 16.0,
        })
        self.Allocation.create({
            'resource_id': machine.id,
            'date_start': '2026-08-01',
            'hours': 8.0,
        })
        self.assertEqual(machine.utilization, 50.0)

    def test_06_task_allocated_hours(self):
        task = self.env['project.task'].create({
            'name': 'Design Review',
        })
        self.Allocation.create({
            'resource_id': self.resource.id,
            'task_id': task.id,
            'date_start': '2026-08-01',
            'hours': 6.0,
        })
        self.assertEqual(task.allocated_hours_total, 6.0)

    def test_07_open_allocations_action(self):
        action = self.resource.action_open_allocations()
        self.assertEqual(action['res_model'], 'sf.resource.planning.allocation')

    def test_08_allocations_company(self):
        alloc = self.Allocation.create({
            'resource_id': self.resource.id,
            'date_start': '2026-08-01',
            'hours': 2.0,
        })
        self.assertTrue(alloc.company_id)