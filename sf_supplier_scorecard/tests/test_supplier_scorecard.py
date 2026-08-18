# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestSupplierScorecard(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Scorecard = self.env['sf.supplier.scorecard']
        self.Issue = self.env['sf.supplier.issue']
        self.partner = self.env['res.partner'].create({'name': 'Vendor Inc'})

    def _make(self, **kw):
        vals = {'partner_id': self.partner.id}
        vals.update(kw)
        return self.Scorecard.create(vals)

    def test_01_scorecard_creation(self):
        sc = self._make()
        self.assertEqual(sc.state, 'draft')
        self.assertEqual(sc.overall_score, 0.0)
        self.assertEqual(sc.rating, 'poor')

    def test_02_overall_equals_kpis(self):
        sc = self._make(on_time_pct=100.0, defect_rate=0.0,
                        quality_score=100.0, compliance_score=100.0)
        self.assertEqual(sc.overall_score, 100.0)
        self.assertEqual(sc.rating, 'excellent')

    def test_03_mid_rating(self):
        sc = self._make(on_time_pct=80.0, defect_rate=10.0,
                        quality_score=80.0, compliance_score=70.0)
        # quality = 100-10 = 90
        score = (80*30 + 90*30 + 80*25 + 70*15) / 100.0
        self.assertEqual(sc.overall_score, score)
        self.assertEqual(sc.rating, 'good')

    def test_04_fair_rating(self):
        sc = self._make(on_time_pct=70.0, defect_rate=20.0,
                        quality_score=65.0, compliance_score=50.0)
        self.assertEqual(sc.rating, 'fair')

    def test_05_weights_affect_score(self):
        a = self._make(on_time_pct=100.0, defect_rate=0.0,
                       quality_score=0.0, compliance_score=0.0)
        # all weight on delivery -> high
        self.assertEqual(a.overall_score, 30.0)
        b = self._make(on_time_pct=0.0, defect_rate=0.0,
                       quality_score=100.0, compliance_score=100.0,
                       on_time_weight=0.0, defect_weight=0.0)
        self.assertEqual(b.overall_score, 40.0)

    def test_06_publish(self):
        sc = self._make()
        sc.action_publish()
        self.assertEqual(sc.state, 'published')

    def test_07_issue_creation(self):
        issue = self.Issue.create({
            'partner_id': self.partner.id,
            'issue_type': 'quality',
            'severity': 'high',
        })
        self.assertFalse(issue.resolved)
        issue.action_resolve()
        self.assertTrue(issue.resolved)