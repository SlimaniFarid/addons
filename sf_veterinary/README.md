# Clinique Vétérinaire & Animaux

Veterinary clinic management: animal patients (complete record by
species, breed, age), calendar appointments, vaccination plans
with automatic due-date reminders, and hospitalization follow-up
from admission to discharge.

## Features

- Animal patient records linked to owners (contacts)
- Calendar appointments with draft/confirm/done/cancelled workflow
- Vaccination booklets with computed due dates and automatic
  reminders
- Hospitalization tracking (admission, cage, discharge)
- Per-species statistics and pivot views
- PDF reports: vaccination card and hospitalization report
- Multi-company access rules and manager-only actions

## Installation

Copy the module to your addons path, update the app list and
install **Clinique Vétérinaire & Animaux**.

## Configuration

Assign the groups in Settings > Users:

- **Veterinary User**: patients, appointments, vaccinations and
  hospitalizations.
- **Veterinary Manager**: patient archiving, hospitalization
  cancellation and due-date protocols.

Company settings (Settings > Veterinary):
- Default durations and vaccination due-date protocols.

## Usage

1. Create animal patients with species, breed and owner.
2. Plan calendar appointments (draft → confirm → done).
3. Record vaccinations; the next due date is computed.
4. The cron creates deduplicated reminders for due vaccines.
5. Admit patients to hospitalization and track until discharge.
6. Generate vaccination and hospitalization PDF reports.

## Permissions

- `sf_veterinary.group_sf_veterinary_user` — read/write on
  business models within the company.
- `sf_veterinary.group_sf_veterinary_manager` — archiving
  patients, cancelling hospitalizations and configuring
  due-date protocols.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).
