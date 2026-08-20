# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase


class TestServiceContracts(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Contract = self.env['sf.service.contract']
        self.Tier = self.env['sf.sla.tier']
        self.Event = self.env['sf.sla.event']
        self.Partner = self.env['res.partner']
        self.partner = self.Partner.create({'name': 'Client A'})
        self.tier = self.Tier.create({
            'name': 'Silver',
            'code': 'SILVER',
            'response_hours': 4,
            'resolution_hours': 24,
        })

    def test_01_tier_creation(self):
        self.assertEqual(self.tier.code, 'SILVER')
        self.assertEqual(self.tier.response_hours, 4)

    def test_02_tier_code_unique(self):
        with self.assertRaises(Exception):
            self.Tier.create({'name': 'Silver X', 'code': 'SILVER'})

    def test_03_contract_creation(self):
        contract = self.Contract.create({
            'name': 'Support Plan',
            'partner_id': self.partner.id,
            'sla_tier_id': self.tier.id,
            'date_start': '2026-01-01',
            'date_end': '2026-12-31',
            'recurring_amount': 500.0,
        })
        self.assertEqual(contract.state, 'draft')
        self.assertEqual(contract.recurring_amount, 500.0)

    def test_04_contract_required_partner(self):
        with self.assertRaises(Exception):
            self.Contract.create({'name': 'No Partner', 'date_start': '2026-01-01'})

    def test_05_contract_workflow(self):
        contract = self.Contract.create({
            'name': 'Support Plan',
            'partner_id': self.partner.id,
            'sla_tier_id': self.tier.id,
            'date_start': '2026-01-01',
        })
        contract.action_activate()
        self.assertEqual(contract.state, 'active')
        contract.action_cancel()
        self.assertEqual(contract.state, 'cancelled')

    def test_06_contract_expiry(self):
        contract = self.Contract.create({
            'name': 'Expired Plan',
            'partner_id': self.partner.id,
            'date_start': '2020-01-01',
            'date_end': '2020-12-31',
        })
        contract.state = 'active'
        contract.action_check_expiry()
        self.assertEqual(contract.state, 'expired')

    def test_07_sla_event_targets(self):
        contract = self.Contract.create({
            'name': 'Support Plan',
            'partner_id': self.partner.id,
            'sla_tier_id': self.tier.id,
            'date_start': '2026-01-01',
        })
        event = self.Event.create({
            'contract_id': contract.id,
            'reference': 'TICKET-001',
            'date_opened': datetime(2026, 5, 1, 9, 0, 0),
        })
        self.assertEqual(event.response_hours, 4)
        self.assertEqual(event.resolution_hours, 24)
        self.assertFalse(event.breached)

    def test_08_sla_breach_detection(self):
        contract = self.Contract.create({
            'name': 'Support Plan',
            'partner_id': self.partner.id,
            'sla_tier_id': self.tier.id,
            'date_start': '2026-01-01',
        })
        event = self.Event.create({
            'contract_id': contract.id,
            'reference': 'TICKET-002',
            'date_opened': datetime(2026, 5, 1, 9, 0, 0),
            'date_responded': datetime(2026, 5, 2, 15, 0, 0),
        })
        # responded 30h later vs 4h target -> breach
        self.assertTrue(event.response_breached)
        self.assertTrue(event.breached)
        self.assertEqual(contract.breached_events, 1)