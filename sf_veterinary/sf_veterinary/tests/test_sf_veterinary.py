# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfVeterinary(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Patient = self.env['sf.veterinary.patient']
        self.Appointment = self.env['sf.veterinary.appointment']
        self.Vaccination = self.env['sf.veterinary.vaccination']
        self.Hospitalization = self.env['sf.veterinary.hospitalization']
        self.group_user = self.env.ref('sf_veterinary.group_sf_veterinary_user')
        self.group_manager = self.env.ref(
            'sf_veterinary.group_sf_veterinary_manager')
        self.user = self.env['res.users'].create({
            'name': 'Veterinary User',
            'login': 'veterinary_user',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Veterinary Manager',
            'login': 'veterinary_manager',
            'groups_id': [(4, self.group_manager.id)],
        })
        self.owner = self.env['res.partner'].create({'name': 'John Owner'})

    def _create_patient(self):
        return self.Patient.create({
            'species': 'dog',
            'breed': 'Labrador',
            'gender': 'male',
            'birth_date': fields.Date.today() - timedelta(days=365),
            'owner_id': self.owner.id,
            'weight_kg': 25.0,
        })

    def test_create_records_with_sequences(self):
        patient = self._create_patient()
        self.assertTrue(patient.name.startswith('PAT-'))
        patient.action_activate()
        appointment = self.Appointment.create({
            'patient_id': patient.id,
            'veterinarian_id': self.owner.id,
            'start_datetime': fields.Datetime.now() + timedelta(days=1),
        })
        self.assertTrue(appointment.name.startswith('RDV-'))
        vaccination = self.Vaccination.create({
            'patient_id': patient.id,
            'vaccine_name': 'Rabies',
        })
        self.assertTrue(vaccination.name.startswith('VAC-'))
        hospitalization = self.Hospitalization.create({
            'patient_id': patient.id,
            'reason': 'Surgery follow-up',
        })
        self.assertTrue(hospitalization.name.startswith('HOS-'))

    def test_age_months_stored(self):
        today = fields.Date.today()
        patient = self.Patient.create({
            'species': 'cat',
            'gender': 'female',
            'birth_date': today.replace(year=today.year - 1),
            'owner_id': self.owner.id,
        })
        self.assertEqual(patient.age_months, 12)

    def test_vaccinations_ok_stored(self):
        patient = self._create_patient()
        self.assertFalse(patient.vaccinations_ok)
        vaccination = self.Vaccination.create({
            'patient_id': patient.id,
            'vaccine_name': 'Rabies',
            'administered_date': fields.Date.today() - timedelta(days=30),
        })
        vaccination.action_administer()
        patient.invalidate_recordset()
        self.assertTrue(patient.vaccinations_ok)

    def test_appointment_past_date_user_error(self):
        patient = self._create_patient()
        with self.assertRaises(UserError):
            self.Appointment.create({
                'patient_id': patient.id,
                'start_datetime': fields.Datetime.now() - timedelta(days=1),
            })

    def test_vaccination_without_patient_user_error(self):
        with self.assertRaises(UserError):
            self.Vaccination.create({'vaccine_name': 'Rabies'})

    def test_vaccination_duplicate_user_error(self):
        patient = self._create_patient()
        self.Vaccination.create({
            'patient_id': patient.id,
            'vaccine_name': 'Rabies',
        })
        with self.assertRaises(UserError):
            self.Vaccination.create({
                'patient_id': patient.id,
                'vaccine_name': 'Rabies',
            })

    def test_hospitalization_discharge_before_admission_user_error(self):
        patient = self._create_patient()
        hospitalization = self.Hospitalization.create({
            'patient_id': patient.id,
            'reason': 'Observation',
        })
        hospitalization.action_confirm()
        hospitalization.discharge_date = fields.Datetime.now() - timedelta(
            days=1)
        with self.assertRaises(UserError):
            hospitalization.action_discharge()

    def test_archive_patient_reserved_to_manager(self):
        patient = self._create_patient()
        patient.action_activate()
        with self.assertRaises(UserError):
            patient.with_user(self.user).action_archive_patient()
        patient.with_user(self.manager).action_archive_patient()
        self.assertEqual(patient.state, 'archived')

    def test_cancel_hospitalization_reserved_to_manager(self):
        patient = self._create_patient()
        hospitalization = self.Hospitalization.create({
            'patient_id': patient.id,
            'reason': 'Observation',
        })
        with self.assertRaises(UserError):
            hospitalization.with_user(self.user).action_cancel()
        hospitalization.with_user(self.manager).action_cancel()
        self.assertEqual(hospitalization.state, 'cancelled')

    def test_cron_vaccination_reminder_dedup(self):
        patient = self._create_patient()
        vaccination = self.Vaccination.create({
            'patient_id': patient.id,
            'vaccine_name': 'Rabies',
            'administered_date': fields.Date.today() - timedelta(days=370),
        })
        vaccination.action_administer()
        self.env.company.sf_veterinary_reminder_days = 7
        vaccination._cron_vaccination_reminders()
        vaccination._cron_vaccination_reminders()
        todo = self.env.ref('mail.mail_activity_data_todo')
        activities = vaccination.activity_ids.filtered(
            lambda a: a.activity_type_id == todo and not a.done)
        self.assertEqual(len(activities), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create(
            {'name': 'Veterinary Company B'})
        patient = self.Patient.with_company(company_b).create({
            'species': 'cat',
            'gender': 'female',
            'owner_id': self.owner.id,
        })
        found = self.Patient.with_user(self.user).search(
            [('id', '=', patient.id)])
        self.assertNotIn(patient, found)

    def test_reports_render(self):
        patient = self._create_patient()
        patient.action_activate()
        vaccination = self.Vaccination.create({
            'patient_id': patient.id,
            'vaccine_name': 'Rabies',
        })
        vaccination.action_administer()
        report = self.env.ref(
            'sf_veterinary.report_sf_veterinary_vaccination_card')
        result = report._render_qweb_html(patient.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Vaccination Card', html)
        hospitalization = self.Hospitalization.create({
            'patient_id': patient.id,
            'reason': 'Observation',
        })
        hospitalization.action_confirm()
        hospitalization.action_discharge()
        hospitalization_report = self.env.ref(
            'sf_veterinary.report_sf_veterinary_hospitalization')
        result = hospitalization_report._render_qweb_html(hospitalization.ids)
        html = result[0]
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        self.assertIn('Hospitalization Report', html)
