# Medical Practice & Patients

Lightweight patient files, a conflict-free appointment agenda,
consultations with diagnosis, prescriptions with dosage and computed
vital signs (BMI) for medical practices.

## Features

- Centralized patient files (identity, allergies, insurance)
- Sequential numbering for patients, appointments, consultations,
  prescriptions and vital signs
- Appointment agenda without overlapping slots per practitioner
- Consultations with diagnosis (draft → done → closed)
- Prescriptions with dosage (draft → issued → closed)
- Vital signs with computed BMI
- Automated reminder activities for unconfirmed appointments
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Medical Practice & Patients**.

## Configuration

Assign the groups in Settings > Users:

- **Medical User**: patients, appointments and vital signs.
- **Medical Manager**: full access, closing consultations and
  prescriptions, all companies.

Company settings (Settings > Medical):
- Number of days before an appointment is reminded if not confirmed.

## Usage

1. Create the patient file.
2. Schedule an appointment (conflicts are prevented).
3. Record the consultation with diagnosis.
4. Issue prescriptions with dosage.
5. Record vital signs; the BMI is computed automatically.

## Permissions

- `sf_medical_practice.group_sf_medical_user` — read/write limited.
- `sf_medical_practice.group_sf_medical_manager` — full access,
  closing consultations and prescriptions.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).