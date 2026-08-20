# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestPackagingConsigns(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Type = self.env['sf.packaging.type']
        self.Site = self.env['sf.packaging.site']
        self.Park = self.env['sf.packaging.park']
        self.Move = self.env['sf.packaging.move']
        self.Return = self.env['sf.packaging.return']
        self.group_user = self.env.ref(
            'sf_packaging_consigns.group_packaging_user')
        self.group_manager = self.env.ref(
            'sf_packaging_consigns.group_packaging_manager')
        self.env.user.groups_id |= self.group_manager
        self.partner = self.env['res.partner'].create({'name': 'Client A'})

    def _create_type(self, deposit_amount=0.5, min_stock=10):
        return self.Type.create({
            'product_name': 'Bottle 75cl',
            'condition': 6,
            'deposit_amount': deposit_amount,
            'min_stock': min_stock,
        })

    def _create_site(self):
        return self.Site.create({'name': 'Main Warehouse',
                                 'address': '1 Depot Street'})

    def _create_park(self, ptype=None, site=None, quantity=0):
        return self.Park.create({
            'packaging_type_id': (ptype or self._create_type()).id,
            'site_id': (site or self._create_site()).id,
            'quantity': quantity,
        })

    def _create_move(self, ptype=None, site=None, quantity=10,
                     partner=None):
        return self.Move.create({
            'packaging_type_id': (ptype or self._create_type()).id,
            'site_id': (site or self._create_site()).id,
            'partner_id': (partner or self.partner).id,
            'quantity': quantity,
            'reference': 'DEL-0001',
        })

    def _create_return(self, ptype=None, site=None, quantity=4,
                       partner=None):
        return self.Return.create({
            'packaging_type_id': (ptype or self._create_type()).id,
            'site_id': (site or self._create_site()).id,
            'partner_id': (partner or self.partner).id,
            'quantity': quantity,
            'received_ok': quantity,
        })

    def _create_user(self, name='Packaging User', login='packaging_user',
                     group=None):
        return self.env['res.users'].create({
            'name': name,
            'login': login,
            'groups_id': [(4, (group or self.group_user).id)],
        })

    def test_create_records_with_sequences(self):
        ptype = self._create_type()
        self.assertTrue(ptype.name.startswith('PKG-'))
        site = self._create_site()
        self.assertTrue(site.name.startswith('SIT-'))
        park = self._create_park(ptype=ptype, site=site)
        self.assertTrue(park.name.startswith('PRK-'))
        move = self._create_move(ptype=ptype, site=site)
        self.assertTrue(move.name.startswith('MOV-'))
        ret = self._create_return(ptype=ptype, site=site)
        self.assertTrue(ret.name.startswith('RET-'))

    def test_deposit_total_computed(self):
        ptype = self._create_type(deposit_amount=0.5)
        move = self._create_move(ptype=ptype, quantity=10)
        self.assertEqual(move.deposit_total, 5.0)
        ret = self._create_return(ptype=ptype, quantity=4)
        self.assertEqual(ret.deposit_total, 2.0)

    def test_park_balance_after_move_and_return(self):
        ptype = self._create_type(deposit_amount=0.5, min_stock=1)
        site = self._create_site()
        move = self._create_move(ptype=ptype, site=site, quantity=10)
        move.action_done()
        park = self.Park.search([
            ('packaging_type_id', '=', ptype.id),
            ('site_id', '=', site.id),
        ])
        self.assertTrue(park)
        self.assertEqual(park.available_quantity, 10)
        self.assertEqual(park.move_done_qty, 10)
        self.assertEqual(park.quantity, 10)
        ret = self._create_return(ptype=ptype, site=site, quantity=4)
        ret.action_received()
        park._compute_balance()
        self.assertEqual(park.available_quantity, 6)
        self.assertEqual(park.return_received_qty, 4)
        self.assertEqual(park.return_rate, 40.0)

    def test_return_exceeding_partner_balance(self):
        ptype = self._create_type(deposit_amount=0.5)
        site = self._create_site()
        move = self._create_move(ptype=ptype, site=site, quantity=10)
        move.action_done()
        ret = self._create_return(ptype=ptype, site=site, quantity=15)
        with self.assertRaises(UserError):
            ret.action_received()

    def test_close_move_requires_manager(self):
        ptype = self._create_type(deposit_amount=0.5)
        site = self._create_site()
        move = self._create_move(ptype=ptype, site=site, quantity=10)
        move.action_done()
        user = self._create_user(login='packaging_user_close',
                                 group=self.group_user)
        with self.assertRaises(UserError):
            move.with_user(user).action_close()

    def test_cron_alert_with_dedup(self):
        ptype = self._create_type(min_stock=20)
        site = self._create_site()
        park = self._create_park(ptype=ptype, site=site, quantity=5)
        park._check_packaging_alerts()
        self.assertTrue(park.activity_ids)
        count_before = len(park.activity_ids)
        park._check_packaging_alerts()
        self.assertEqual(len(park.activity_ids), count_before)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'Packaging Company B'})
        user = self._create_user(name='Packaging Company A User',
                                 login='packaging_company_a_user',
                                 group=self.group_user)
        ptype = self.Type.with_company(company_b).create({
            'product_name': 'Bottle B',
            'condition': 12,
            'deposit_amount': 0.25,
            'min_stock': 5,
        })
        self.assertNotIn(ptype, self.Type.with_user(user).search(
            [('id', '=', ptype.id)]))

    def test_report_records_exist(self):
        reports = self.env['ir.actions.report'].search([
            ('report_name', 'in', [
                'sf_packaging_consigns.report_followup_template',
                'sf_packaging_consigns.report_parks_template',
            ])])
        self.assertEqual(len(reports), 2)