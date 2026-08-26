# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestRealEstate(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Property = self.env['sf.realestate.property']
        self.Lease = self.env['sf.realestate.lease']
        self.RentInvoice = self.env['sf.realestate.rent.invoice']
        self.Partner = self.env['res.partner']
        self.tenant = self.Partner.create({'name': 'Jane Tenant'})
        self.owner = self.Partner.create({'name': 'Bob Owner'})
        self.property = self.Property.create({
            'name': 'Sunset Apartment',
            'code': 'APT-001',
            'property_type': 'apartment',
            'owner_id': self.owner.id,
            'value': 250000.0,
            'surface': 85.0,
        })

    def test_01_property_creation(self):
        self.assertEqual(self.property.state, 'available')
        self.assertEqual(self.property.code, 'APT-001')
        self.assertTrue(self.property.currency_id)

    def test_02_property_code_unique(self):
        with self.assertRaises(Exception):
            self.Property.create({
                'name': 'Other',
                'code': 'APT-001',
            })

    def test_03_lease_sequence_and_state(self):
        lease = self.Lease.create({
            'property_id': self.property.id,
            'tenant_id': self.tenant.id,
            'date_start': '2026-01-01',
            'rent': 1200.0,
        })
        self.assertTrue(lease.name)
        self.assertNotEqual(lease.name, '/')
        self.assertEqual(lease.state, 'draft')

    def test_04_activate_lease_sets_property_rented(self):
        lease = self.Lease.create({
            'property_id': self.property.id,
            'tenant_id': self.tenant.id,
            'date_start': '2026-01-01',
            'rent': 1200.0,
        })
        lease.action_activate()
        self.assertEqual(lease.state, 'active')
        self.assertEqual(self.property.state, 'rented')
        self.assertEqual(self.property.occupancy, 100.0)
        self.assertEqual(self.property.monthly_rent, 1200.0)

    def test_05_close_lease_frees_property(self):
        lease = self.Lease.create({
            'property_id': self.property.id,
            'tenant_id': self.tenant.id,
            'date_start': '2026-01-01',
            'rent': 1200.0,
        })
        lease.action_activate()
        lease.action_close()
        self.assertEqual(lease.state, 'closed')
        self.assertEqual(self.property.state, 'available')

    def test_06_generate_rent_invoices(self):
        lease = self.Lease.create({
            'property_id': self.property.id,
            'tenant_id': self.tenant.id,
            'date_start': '2026-01-01',
            'rent': 1000.0,
        })
        lease.action_activate()
        lease.action_generate_invoices(2)
        self.assertEqual(len(lease.invoice_ids), 2)
        self.assertEqual(lease.total_invoiced, 2000.0)

    def test_07_rent_invoice_workflow(self):
        lease = self.Lease.create({
            'property_id': self.property.id,
            'tenant_id': self.tenant.id,
            'date_start': '2026-01-01',
            'rent': 900.0,
        })
        lease.action_activate()
        lease.action_generate_invoices(1)
        invoice = lease.invoice_ids[0]
        self.assertEqual(invoice.state, 'draft')
        invoice.action_post()
        self.assertEqual(invoice.state, 'posted')
        invoice.action_paid()
        self.assertEqual(invoice.state, 'paid')
        self.assertEqual(lease.total_paid, 900.0)

    def test_08_property_status_buttons(self):
        self.property.action_maintenance()
        self.assertEqual(self.property.state, 'maintenance')
        self.property.action_available()
        self.assertEqual(self.property.state, 'available')