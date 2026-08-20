# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestMedicalPractice(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Patient = self.env['sf.medical.patient']
        self.Appointment = self.env['sf.medical.appointment']
        self.Consultation = self.env['sf.medical.consultation']
        self.Prescription = self.env['sf.medical.prescription']
        self.Vital = self.env['sf.medical.vital']
        self.group_user = self.env.ref(
            'sf_medical_practice.group_sf_medical_user')
        self.group_manager = self.env.ref(
            'sf_medical_practice.group_sf_medical_manager')
        self.user = self.env['res.users'].create({
            'name': 'Medical User',
            'login': 'medical_user',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Medical Manager',
            'login': 'medical_manager',
            'groups_id': [(4, self.group_manager.id)],
        })

    def _create_patient(self, firstname='John', lastname='Doe'):
        return self.Patient.create({
            'firstname': firstname,
            'lastname': lastname,
            'dob': fields.Date.today() - timedelta(days=365 * 30),
            'gender': 'male',
            'phone': '123456789',
            'email': '%s.%s@example.com' % (firstname.lower(),
                                            lastname.lower()),
            'blood_type': 'o+',
            'insurance': 'INS-001',
            'allergies': 'None',
        })

    def _create_appointment(self, patient, start_time=9.0, duration=0.5,
                            date=None, state='draft'):
        return self.Appointment.create({
            'patient_id': patient.id,
            'practitioner_id': self.user.id,
            'date': date or fields.Date.context_today(
                self.env['sf.medical.appointment']),
            'start_time': start_time,
            'duration': duration,
            'reason': 'Check-up',
            'state': state,
        })

    def _create_consultation(self, patient):
        return self.Consultation.create({
            'patient_id': patient.id,
            'practitioner_id': self.user.id,
            'date': fields.Date.context_today(
                self.env['sf.medical.consultation']),
            'diagnosis': 'Healthy',
            'notes': 'No issues',
        })

    def _create_prescription(self, consultation):
        return self.Prescription.create({
            'consultation_id': consultation.id,
            'medication': 'Paracetamol',
            'dosage': '500mg twice a day',
            'duration_days': 7,
        })

    def _create_vital(self, patient, weight=70.0, height=175.0):
        return self.Vital.create({
            'patient_id': patient.id,
            'date': fields.Date.context_today(self.env['sf.medical.vital']),
            'weight': weight,
            'height': height,
            'blood_pressure': '120/80',
        })

    def test_create_models_with_sequences(self):
        patient = self._create_patient()
        self.assertTrue(patient.name.startswith('PAT-'))
        appointment = self._create_appointment(patient)
        self.assertTrue(appointment.name.startswith('APT-'))
        consultation = self._create_consultation(patient)
        self.assertTrue(consultation.name.startswith('CNS-'))
        prescription = self._create_prescription(consultation)
        self.assertTrue(prescription.name.startswith('PRS-'))
        vital = self._create_vital(patient)
        self.assertTrue(vital.name.startswith('VTL-'))

    def test_appointment_conflict(self):
        patient = self._create_patient()
        self._create_appointment(patient, start_time=9.0, duration=1.0)
        with self.assertRaises(UserError):
            self._create_appointment(patient, start_time=9.5, duration=1.0)

    def test_confirm_appointment_conflict(self):
        patient = self._create_patient()
        first = self._create_appointment(patient, start_time=9.0,
                                         duration=1.0, state='scheduled')
        second = self._create_appointment(patient, start_time=10.0,
                                          duration=1.0, state='scheduled')
        second.write({'start_time': 9.5})
        with self.assertRaises(UserError):
            second.action_confirm()

    def test_bmi_calculation(self):
        vital = self._create_vital(self._create_patient(), weight=70.0,
                                   height=175.0)
        self.assertAlmostEqual(vital.bmi, 70.0 / (1.75 ** 2), places=2)
        zero = self._create_vital(self._create_patient(), weight=70.0,
                                  height=0.0)
        self.assertEqual(zero.bmi, 0)

    def test_consultation_close_non_manager(self):
        consultation = self._create_consultation(self._create_patient())
        with self.assertRaises(UserError):
            consultation.with_user(self.user).action_done()
        with self.assertRaises(UserError):
            consultation.with_user(self.user).action_close()

    def test_consultation_close_manager(self):
        consultation = self._create_consultation(self._create_patient())
        consultation.with_user(self.manager).action_done()
        self.assertEqual(consultation.state, 'done')
        consultation.with_user(self.manager).action_close()
        self.assertEqual(consultation.state, 'closed')

    def test_prescription_closed_non_manager(self):
        consultation = self._create_consultation(self._create_patient())
        prescription = self._create_prescription(consultation)
        prescription.with_user(self.user).action_issue()
        self.assertEqual(prescription.state, 'issued')
        with self.assertRaises(UserError):
            prescription.with_user(self.user).action_close()
        prescription.with_user(self.manager).action_close()
        self.assertEqual(prescription.state, 'closed')

    def test_cron_reminder_dedup(self):
        patient = self._create_patient()
        appointment = self._create_appointment(patient, start_time=9.0,
                                               state='scheduled')
        self.Appointment._check_appointment_reminders()
        self.Appointment._check_appointment_reminders()
        self.assertEqual(len(appointment.activity_ids), 1)
        self.assertEqual(
            appointment.activity_ids.activity_type_id,
            self.env.ref('mail.mail_activity_data_todo'))

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create(
            {'name': 'Medical Practice Company B'})
        patient = self._create_patient()
        other = self.Patient.with_company(company_b).create({
            'firstname': 'Jane',
            'lastname': 'Smith',
        })
        self.assertNotIn(other, self.Patient.with_user(self.user).search(
            [('id', '=', other.id)]))
        self.assertIn(patient, self.Patient.with_user(self.user).search(
            [('id', '=', patient.id)]))

    def test_reports_render(self):
        patient = self._create_patient()
        consultation = self._create_consultation(patient)
        self._create_prescription(consultation)
        for report in (
            self.env.ref('sf_medical_practice.report_medical_patient_file'),
            self.env.ref('sf_medical_practice.report_medical_ordonnance'),
        ):
            docids = patient.ids if report.model == 'sf.medical.patient' \
                else consultation.prescription_ids.ids
            self.assertTrue(docids)
            result = report._render_qweb_pdf(docids)
            content = result[0] if isinstance(result, tuple) else result
            self.assertTrue(content)