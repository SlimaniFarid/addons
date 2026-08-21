# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestLeadScore(TransactionCase):

    def setUp(self):
        super().setUp()
        self.company = self.env.company

    def test_create_record(self):
        Model = self.env['sf.lead.scoring.ai.scoring.rule']
        rec = Model.create({'name': 'Test %s' % uuid.uuid4().hex[:6]})
        self.assertTrue(rec.id)
        self.assertTrue(rec.name)

    def test_workflow(self):
        Model = self.env['sf.lead.scoring.ai.scoring.rule']
        rec = Model.create({'name': 'WF %s' % uuid.uuid4().hex[:6]})
        self.assertTrue(hasattr(rec, 'state'))

    def test_company_isolation(self):
        co2 = self.env['res.company'].create({'name': 'Co Test'})
        Model = self.env['sf.lead.scoring.ai.scoring.rule']
        r1 = Model.create({'name': 'C1'})
        r2 = Model.with_company(co2).create({'name': 'C2', 'company_id': co2.id})
        user = self.env['res.users'].create({
            'name': 'U', 'login': 'u_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [])],
            'company_ids': [(6, 0, [self.company.id])],
        })
        self.assertTrue(r1.with_user(user).exists())
        self.assertFalse(r2.with_user(user).exists())
