# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo import fields


class TestSalesRoutes(TransactionCase):

    def setUp(self):
        super().setUp()
        self.territory = self.env['sf.route.territory'].create({
            'name': 'North Region',
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Visit Customer',
        })
        self.tour = self.env['sf.route.tour'].create({
            'name': 'Tour 001',
            'date': fields.Date.today(),
            'territory_id': self.territory.id,
        })
        self.visit = self.env['sf.route.visit'].create({
            'tour_id': self.tour.id,
            'partner_id': self.partner.id,
            'sequence': 1,
        })

    def test_tour_workflow(self):
        self.assertEqual(self.tour.state, 'draft')
        self.tour.action_plan()
        self.assertEqual(self.tour.state, 'planned')
        self.tour.action_start()
        self.assertEqual(self.tour.state, 'in_progress')
        self.tour.action_complete()
        self.assertEqual(self.tour.state, 'completed')

    def test_tour_complete_requires_in_progress(self):
        self.tour.action_plan()
        with self.assertRaises(UserError):
            self.tour.action_complete()

    def test_visit_check_in_out(self):
        self.visit.action_check_in()
        self.assertEqual(self.visit.state, 'in_progress')
        self.assertTrue(self.visit.check_in)
        self.visit.action_check_out()
        self.assertEqual(self.visit.state, 'done')
        self.assertTrue(self.visit.check_out)

    def test_visit_missed(self):
        self.visit.action_mark_missed()
        self.assertEqual(self.visit.state, 'missed')

    def test_visit_check_out_requires_check_in(self):
        with self.assertRaises(UserError):
            self.visit.action_check_out()

    def test_create_order_from_done_visit(self):
        self.visit.action_check_in()
        self.visit.action_check_out()
        result = self.visit.action_create_order()
        self.assertEqual(result['res_model'], 'sale.order')
        self.assertTrue(self.visit.sale_order_id)
        self.assertEqual(self.visit.result, 'order')

    def test_duplicate_partner_in_tour_blocked(self):
        with self.assertRaises(Exception):
            self.env['sf.route.visit'].create({
                'tour_id': self.tour.id,
                'partner_id': self.partner.id,
            })

    def test_missed_visit_cron(self):
        self.visit.action_mark_missed()
        self.visit._check_missed_visits()
        self.assertEqual(self.visit.state, 'missed')