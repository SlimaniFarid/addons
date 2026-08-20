# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestExportDocuments(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Dossier = self.env['sf.export.dossier']
        self.Incoterm = self.env['sf.export.incoterm']
        self.group_user = self.env.ref(
            'sf_export_documents.group_export_user')
        self.partner = self.env['res.partner'].create({'name': 'Foreign Buyer'})
        self.country = self.env['res.country'].create({'name': 'France',
                                                       'code': 'FR'})
        self.buyer_country = self.env['res.country'].create({
            'name': 'Morocco', 'code': 'MA'})
        self.incoterm = self.Incoterm.create({'code': 'FOB',
                                              'name': 'Free On Board'})

    def _create_dossier(self, state='draft'):
        return self.Dossier.create({
            'partner_id': self.partner.id,
            'destination_country_id': self.buyer_country.id,
            'origin_country_id': self.country.id,
            'incoterm_id': self.incoterm.id,
            'transport_mode': 'sea',
            'state': state,
        })

    def test_create_dossier_with_sequence(self):
        dossier = self._create_dossier()
        self.assertTrue(dossier.name.startswith('EXP-'))
        self.assertEqual(dossier.origin_country_id, self.country)

    def test_incoterm_defaults(self):
        incoterm = self.env.ref('sf_export_documents.incoterm_fob')
        self.assertEqual(incoterm.code, 'FOB')

    def test_preparation_flow(self):
        dossier = self._create_dossier()
        dossier.action_start_preparation()
        self.assertEqual(dossier.state, 'in_preparation')

    def test_ready_with_incomplete_docs(self):
        dossier = self._create_dossier()
        dossier.action_start_preparation()
        dossier.doc_invoice_ok = True
        with self.assertRaises(UserError):
            dossier.action_mark_ready()

    def test_ready_with_complete_docs(self):
        dossier = self._create_dossier()
        dossier.action_start_preparation()
        dossier.write({
            'doc_invoice_ok': True,
            'doc_packing_ok': True,
            'doc_origin_ok': True,
            'doc_eur_ok': True,
        })
        self.assertEqual(dossier.completeness, 4)
        dossier.action_mark_ready()
        self.assertEqual(dossier.state, 'ready')

    def test_shipped_requires_ready(self):
        dossier = self._create_dossier()
        with self.assertRaises(UserError):
            dossier.action_mark_shipped()

    def test_shipped_flow(self):
        dossier = self._create_dossier()
        dossier.action_start_preparation()
        dossier.write({
            'doc_invoice_ok': True,
            'doc_packing_ok': True,
            'doc_origin_ok': True,
            'doc_eur_ok': True,
        })
        dossier.action_mark_ready()
        dossier.action_mark_shipped()
        self.assertEqual(dossier.state, 'shipped')
        self.assertTrue(dossier.shipped_date)

    def test_archive_flow(self):
        dossier = self._create_dossier()
        dossier.action_start_preparation()
        dossier.write({
            'doc_invoice_ok': True,
            'doc_packing_ok': True,
            'doc_origin_ok': True,
            'doc_eur_ok': True,
        })
        dossier.action_mark_ready()
        dossier.action_mark_shipped()
        dossier.action_archive()
        self.assertEqual(dossier.state, 'archived')

    def test_delete_in_preparation(self):
        dossier = self._create_dossier()
        dossier.action_start_preparation()
        with self.assertRaises(UserError):
            dossier.unlink()

    def test_cancel_flow(self):
        dossier = self._create_dossier()
        dossier.action_start_preparation()
        dossier.action_cancel()
        self.assertEqual(dossier.state, 'cancelled')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Export Company B'})
        user = self.env['res.users'].create({
            'name': 'Export Company A User',
            'login': 'export_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Dossier.with_company(company_b).create({
            'partner_id': self.partner.id,
            'destination_country_id': self.buyer_country.id,
            'origin_country_id': self.country.id,
            'transport_mode': 'sea',
        })
        self.assertNotIn(other, self.Dossier.with_user(user).search(
            [('id', '=', other.id)]))