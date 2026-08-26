# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestAgriculture(TransactionCase):

    def setUp(self):
        super().setUp()
        self.env.user.groups_id |= self.env.ref(
            'sf_agriculture.group_agri_manager')
        self.group_user = self.env.ref('sf_agriculture.group_agri_user')
        self.Farm = self.env['sf.agri.farm']
        self.Plot = self.env['sf.agri.plot']
        self.Campaign = self.env['sf.agri.campaign']
        self.Culture = self.env['sf.agri.culture']
        self.Operation = self.env['sf.agri.operation']
        self.Treatment = self.env['sf.agri.treatment']
        self.Harvest = self.env['sf.agri.harvest']

    def _create_farm(self, name=False):
        vals = {'address': '123 Farm Road'}
        if name:
            vals['name'] = name
        return self.Farm.create(vals)

    def _create_plot(self, farm=None, area=2.0):
        return self.Plot.create({
            'farm_id': (farm or self._create_farm()).id,
            'area_ha': area,
            'soil_type': 'loam',
            'irrigation': 'rain',
        })

    def _create_campaign(self, farm=None, year=2026):
        return self.Campaign.create({
            'farm_id': (farm or self._create_farm()).id,
            'year': year,
            'start_date': fields.Date.today(),
            'state': 'open',
        })

    def _create_culture(self, campaign=None, plot=None, **kw):
        return self.Culture.create({
            'campaign_id': (campaign or self._create_campaign()).id,
            'plot_id': (plot or self._create_plot()).id,
            'crop': 'wheat',
            'variety': 'Symphony',
            'planted_date': fields.Date.today(),
            'state': 'growing',
            **kw,
        })

    def _create_treatment(self, culture=None, **kw):
        return self.Treatment.create({
            'culture_id': (culture or self._create_culture()).id,
            'treatment_type': 'insecticide',
            'product': 'Testicide',
            'active_ingredient': 'Active A',
            'quantity': 10.0,
            'unit': 'kg',
            'state': 'applied',
            **kw,
        })

    def _create_harvest(self, culture=None, plot=None, **kw):
        return self.Harvest.create({
            'culture_id': (culture or self._create_culture()).id,
            'plot_id': (plot or self._create_plot()).id,
            'harvest_date': fields.Date.today(),
            'quantity': 6000.0,
            'unit': 'kg',
            'quality': 'A',
            **kw,
        })

    def test_create_all_models_with_sequences(self):
        farm = self._create_farm()
        plot = self._create_plot(farm=farm)
        campaign = self._create_campaign(farm=farm)
        culture = self._create_culture(campaign=campaign, plot=plot)
        operation = self.Operation.create({
            'culture_id': culture.id,
            'sequence': 1,
            'name': 'Soil tillage',
            'operation_type': 'tillage',
        })
        treatment = self._create_treatment(culture=culture)
        harvest = self._create_harvest(culture=culture, plot=plot)
        self.assertTrue(farm.name.startswith('FAR-'))
        self.assertTrue(plot.name.startswith('PLT-'))
        self.assertTrue(campaign.name.startswith('CMP-'))
        self.assertTrue(culture.name.startswith('CUL-'))
        self.assertTrue(treatment.name.startswith('TRT-'))
        self.assertTrue(harvest.name.startswith('HAR-'))
        self.assertTrue(operation.name)
        self.assertEqual(operation.culture_id, culture)

    def test_yield_computation(self):
        plot = self._create_plot(area=2.0)
        culture = self._create_culture(plot=plot)
        harvest = self._create_harvest(culture=culture, plot=plot)
        self.assertEqual(harvest.yield_t_ha, 3.0)
        culture.invalidate_recordset(['yield_t_ha'])
        self.assertEqual(culture.yield_t_ha, 3.0)

    def test_withdrawal_alert_and_dedup(self):
        today = fields.Date.today()
        culture = self._create_culture(harvest_date=today + timedelta(days=5))
        treatment = self._create_treatment(
            culture=culture, withdrawal_days=30,
            treatment_date=today, state='applied')
        self.Treatment._check_agri_alerts()
        self.assertTrue(treatment.activity_ids)
        count = len(treatment.activity_ids)
        self.Treatment._check_agri_alerts()
        self.assertEqual(len(treatment.activity_ids), count)

    def test_campaign_close_requires_closed_cultures(self):
        campaign = self._create_campaign()
        self._create_culture(campaign=campaign)
        with self.assertRaises(UserError):
            campaign.action_close()

    def test_campaign_close_success(self):
        campaign = self._create_campaign()
        culture = self._create_culture(campaign=campaign)
        culture.state = 'closed'
        campaign.action_close()
        self.assertEqual(campaign.state, 'closed')

    def test_campaign_close_manager_only(self):
        campaign = self._create_campaign()
        culture = self._create_culture(campaign=campaign)
        culture.state = 'closed'
        user = self.env['res.users'].create({
            'name': 'Agri User No Manager',
            'login': 'agri_user_no_manager',
            'groups_id': [(4, self.group_user.id)],
        })
        with self.assertRaises(UserError):
            campaign.with_user(user).action_close()

    def test_harvest_recorded_manager_guard(self):
        harvest = self._create_harvest()
        user = self.env['res.users'].create({
            'name': 'Agri User No Manager',
            'login': 'agri_user_harvest',
            'groups_id': [(4, self.group_user.id)],
        })
        with self.assertRaises(UserError):
            harvest.with_user(user).action_record()
        harvest.action_record()
        self.assertEqual(harvest.state, 'recorded')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Agri Company B'})
        user = self.env['res.users'].create({
            'name': 'Agri Company A User',
            'login': 'agri_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        self._create_farm()
        other = self.Farm.with_company(company_b).create({
            'name': 'Other Farm',
            'address': '456 Other Road',
        })
        self.assertNotIn(other, self.Farm.with_user(user).search(
            [('id', '=', other.id)]))

    def test_reports_exist(self):
        register = self.env.ref('sf_agriculture.report_inputs_register')
        campaign_report = self.env.ref('sf_agriculture.report_campaign')
        self.assertEqual(register.report_type, 'qweb-pdf')
        self.assertEqual(register.report_name,
                         'sf_agriculture.report_inputs_register_template')
        self.assertEqual(campaign_report.report_name,
                         'sf_agriculture.report_campaign_template')
        self.assertTrue(self.env['ir.actions.report']._get_report_from_name(
            'sf_agriculture.report_inputs_register_template'))
        self.assertTrue(self.env['ir.actions.report']._get_report_from_name(
            'sf_agriculture.report_campaign_template'))
        self.assertTrue(self.env.ref('sf_agriculture.group_agri_user'))
        self.assertTrue(self.env.ref('sf_agriculture.group_agri_manager'))