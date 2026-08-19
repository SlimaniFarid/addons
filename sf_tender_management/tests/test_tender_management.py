# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionalCase, tagged


@tagged('post_install', '-at_install')
class TestTenderManagement(TransactionalCase):

    def setUp(self):
        super().setUp()
        self.Tender = self.env['sf.tender']
        self.Offer = self.env['sf.tender.offer']
        self.Criterion = self.env['sf.tender.criterion']
        self.group_user = self.env.ref(
            'sf_tender_management.group_tender_user')
        self.supplier_a = self.env['res.partner'].create({'name': 'Supplier A'})
        self.supplier_b = self.env['res.partner'].create({'name': 'Supplier B'})

    def _create_tender(self, state='draft'):
        return self.Tender.create({
            'title': 'Supply of raw material',
            'tender_type': 'rfq',
            'deadline': fields.Datetime.now() + timedelta(days=7),
            'state': state,
        })

    def _create_offer(self, tender, partner):
        return self.Offer.create({
            'tender_id': tender.id,
            'partner_id': partner.id,
            'amount_total': 1000.0,
        })

    def test_create_tender_with_sequence(self):
        tender = self._create_tender()
        self.assertTrue(tender.name.startswith('TND-'))

    def test_publish_and_offer(self):
        tender = self._create_tender()
        tender.action_publish()
        self.assertEqual(tender.state, 'published')
        offer = self._create_offer(tender, self.supplier_a)
        self.assertTrue(offer.name.startswith('OFR-'))
        self.assertTrue(offer.date_submitted)

    def test_evaluation_before_deadline(self):
        tender = self._create_tender()
        tender.action_publish()
        with self.assertRaises(UserError):
            tender.action_start_evaluation()

    def test_weighted_score(self):
        tender = self._create_tender()
        tender.action_publish()
        tender.write({'deadline': fields.Datetime.now() - timedelta(days=1)})
        tender.action_start_evaluation()
        c1 = self.Criterion.create({'tender_id': tender.id, 'name': 'Price',
                                    'weight': 60.0})
        c2 = self.Criterion.create({'tender_id': tender.id, 'name': 'Quality',
                                    'weight': 40.0})
        offer = self._create_offer(tender, self.supplier_a)
        self.env['sf.tender.offer.score'].create({
            'offer_id': offer.id,
            'criterion_id': c1.id,
            'score': 10.0,
        })
        self.env['sf.tender.offer.score'].create({
            'offer_id': offer.id,
            'criterion_id': c2.id,
            'score': 5.0,
        })
        self.assertAlmostEqual(offer.weighted_score, 80.0)

    def test_award_without_justification(self):
        tender = self._create_tender()
        tender.action_publish()
        tender.write({'deadline': fields.Datetime.now() - timedelta(days=1)})
        tender.action_start_evaluation()
        offer = self._create_offer(tender, self.supplier_a)
        wizard = self.env['sf.tender.award.wizard'].create({
            'tender_id': tender.id,
            'offer_id': offer.id,
        })
        with self.assertRaises(UserError):
            wizard.action_award()

    def test_award_flow(self):
        tender = self._create_tender()
        tender.action_publish()
        tender.write({'deadline': fields.Datetime.now() - timedelta(days=1)})
        tender.action_start_evaluation()
        offer = self._create_offer(tender, self.supplier_a)
        other = self._create_offer(tender, self.supplier_b)
        wizard = self.env['sf.tender.award.wizard'].create({
            'tender_id': tender.id,
            'offer_id': offer.id,
            'justification': 'Best price and delivery time',
        })
        wizard.action_award()
        self.assertEqual(tender.state, 'awarded')
        self.assertEqual(tender.winner_offer_id, offer)
        self.assertEqual(offer.state, 'awarded')
        self.assertEqual(other.state, 'rejected')
        tender.action_close()
        self.assertEqual(tender.state, 'closed')

    def test_only_one_awarded(self):
        tender = self._create_tender()
        tender.action_publish()
        tender.write({'deadline': fields.Datetime.now() - timedelta(days=1)})
        tender.action_start_evaluation()
        offer_a = self._create_offer(tender, self.supplier_a)
        offer_b = self._create_offer(tender, self.supplier_b)
        wizard = self.env['sf.tender.award.wizard'].create({
            'tender_id': tender.id,
            'offer_id': offer_a.id,
            'justification': 'Selected',
        })
        wizard.action_award()
        with self.assertRaises(UserError):
            offer_b.state = 'awarded'

    def test_delete_published_tender(self):
        tender = self._create_tender()
        tender.action_publish()
        with self.assertRaises(UserError):
            tender.unlink()

    def test_cancel_flow(self):
        tender = self._create_tender()
        tender.action_publish()
        tender.action_cancel()
        self.assertEqual(tender.state, 'cancelled')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Tender Company B'})
        user = self.env['res.users'].create({
            'name': 'Tender Company A User',
            'login': 'tender_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Tender.with_company(company_b).create({
            'title': 'Other company tender',
            'tender_type': 'rfq',
            'deadline': fields.Datetime.now() + timedelta(days=5),
        })
        self.assertNotIn(other, self.Tender.with_user(user).search(
            [('id', '=', other.id)]))