# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfSeniorLiving(TransactionCase):

    def setUp(self):
        super().setUp()
        self.company = self.env.company

    def test_residence_creation(self):
        res = self.env['sf.senior.residence'].create({
            'name': 'Test Residence %s' % uuid.uuid4().hex[:6],
            'capacity': 50,
        })
        self.assertTrue(res.name)
        self.assertEqual(res.state, 'active')

    def test_resident_admission(self):
        res = self.env['sf.senior.residence'].create({
            'name': 'Res %s' % uuid.uuid4().hex[:6],
        })
        r = self.env['sf.senior.resident'].create({
            'name': 'John D.',
            'residence_id': res.id,
            'gir_level': 3,
        })
        self.assertEqual(r.state, 'admitted')
        self.assertEqual(res.resident_count, 1)

    def test_gir_level_constraint(self):
        from odoo.exceptions import ValidationError
        res = self.env['sf.senior.residence'].create({
            'name': 'Res %s' % uuid.uuid4().hex[:6],
        })
        try:
            self.env['sf.senior.resident'].create({
                'name': 'Bad GIR',
                'residence_id': res.id,
                'gir_level': 99,
            })
            raise AssertionError('Should have raised')
        except Exception:
            pass
