# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestItAssetManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Asset = self.env['sf.it.asset']
        self.License = self.env['sf.it.license']
        self.Assignment = self.env['sf.it.assignment']
        self.LicenseAssign = self.env['sf.it.license.assignment']
        self.employee = self.env['hr.employee'].create({
            'name': 'IT Test Employee',
        })
        self.category = self.env.ref(
            'sf_it_asset_management.it_asset_category_laptop')
        self.manager = self.env['res.users'].create({
            'name': 'IT Manager',
            'login': 'it_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_it_asset_management.group_it_asset_manager').id,
                ]),
            ],
        })
        self.user = self.env['res.users'].create({
            'name': 'IT User',
            'login': 'it_user_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_it_asset_management.group_it_asset_user').id,
                ]),
            ],
        })

    def _make_asset(self, **kw):
        vals = {'name': 'Laptop Test', 'category_id': self.category.id}
        vals.update(kw)
        return self.Asset.create(vals)

    def _make_license(self, **kw):
        vals = {'name': 'Office Suite', 'seats': 5}
        vals.update(kw)
        return self.License.create(vals)

    def test_01_asset_creation(self):
        asset = self._make_asset()
        self.assertEqual(asset.state, 'draft')
        asset.action_to_stock()
        self.assertEqual(asset.state, 'in_stock')

    def test_02_assign_and_unassign(self):
        asset = self._make_asset()
        asset.action_to_stock()
        assignment = self.Assignment.create({
            'asset_id': asset.id,
            'employee_id': self.employee.id,
            'date_from': '2026-01-01',
        })
        self.assertEqual(asset.state, 'assigned')
        self.assertEqual(asset.assignee_id, self.employee)
        assignment.action_close()
        asset._compute_assignment()
        self.assertEqual(asset.state, 'in_stock')
        self.assertFalse(asset.assignee_id)

    def test_03_cannot_assign_assigned_asset(self):
        asset = self._make_asset()
        asset.action_to_stock()
        self.Assignment.create({
            'asset_id': asset.id,
            'employee_id': self.employee.id,
            'date_from': '2026-01-01',
        })
        with self.assertRaises(UserError):
            self.Assignment.create({
                'asset_id': asset.id,
                'employee_id': self.employee.id,
                'date_from': '2026-01-02',
            })

    def test_04_cannot_assign_draft_asset(self):
        asset = self._make_asset()
        with self.assertRaises(UserError):
            self.Assignment.create({
                'asset_id': asset.id,
                'employee_id': self.employee.id,
                'date_from': '2026-01-01',
            })

    def test_05_cannot_retire_assigned_asset(self):
        asset = self._make_asset()
        asset.action_to_stock()
        self.Assignment.create({
            'asset_id': asset.id,
            'employee_id': self.employee.id,
            'date_from': '2026-01-01',
        })
        with self.assertRaises(UserError):
            asset.action_retire()

    def test_06_license_seats(self):
        license = self._make_license()
        license.action_activate()
        self.assertEqual(license.used_seats, 0)
        self.assertEqual(license.available_seats, 5)

    def test_07_license_seat_overflow(self):
        license = self._make_license(seats=2)
        license.action_activate()
        for i in range(2):
            emp = self.env['hr.employee'].create({'name': 'Emp %s' % i})
            self.LicenseAssign.create({
                'license_id': license.id,
                'employee_id': emp.id,
                'date_from': '2026-01-01',
            })
        emp3 = self.env['hr.employee'].create({'name': 'Emp 3'})
        with self.assertRaises(UserError):
            self.LicenseAssign.create({
                'license_id': license.id,
                'employee_id': emp3.id,
                'date_from': '2026-01-01',
            })

    def test_08_license_expired_block(self):
        license = self._make_license()
        license.action_activate()
        license.state = 'expired'
        with self.assertRaises(UserError):
            self.LicenseAssign.create({
                'license_id': license.id,
                'employee_id': self.employee.id,
                'date_from': '2026-01-01',
            })

    def test_09_negative_value_rejected(self):
        with self.assertRaises(UserError):
            self._make_asset(purchase_value=-5.0)

    def test_10_warranty_before_purchase_rejected(self):
        with self.assertRaises(UserError):
            self._make_asset(purchase_date='2026-02-01',
                             warranty_expiration='2026-01-01')

    def test_11_user_cannot_retire(self):
        asset = self._make_asset()
        asset.action_to_stock()
        with self.assertRaises(UserError):
            asset.with_user(self.user).action_retire()

    def test_12_wizard_assign(self):
        asset = self._make_asset()
        asset.action_to_stock()
        wizard = self.env['sf.it.assignment.wizard'].create({
            'asset_id': asset.id,
            'employee_id': self.employee.id,
            'date_from': '2026-01-01',
        })
        wizard.action_assign()
        self.assertEqual(asset.state, 'assigned')
        self.assertEqual(asset.assignee_id, self.employee)