# Occupational Health & Medical Surveillance

Track mandatory medical visits per employee (hire, periodic,
return to work), periodicities by job and exposure, doctors and
practices, aptitude results, validity dates and renewal alerts,
vaccinations and job restrictions, and a compliance dashboard.

## Features

- Per-employee medical surveillance files (one active file per employee)
- Medical visits: planning, scheduling, result recording, validity
- Exposure reasons with default periodicity
- Expiry alerts via daily cron (configurable threshold)
- Optional auto-creation of periodic visits at due date
- Job restrictions and contraindications
- Vaccination records
- Compliance dashboard (graph / pivot)

## Installation

Copy the module to your addons path, update the app list and
install **Occupational Health & Medical Surveillance**.

## Configuration

Assign the groups in Settings > Users:

- **Occupational Health User**: consult files and plan visits.
- **Occupational Health Manager**: full access (results,
  restrictions, configuration, dashboard).

Company settings (Settings > Occupational Health):
- Alert days before expiry.
- Auto-create periodic visits.
- Default visit periodicity (months).

## Usage

1. Create a medical file for an employee.
2. Plan and schedule visits (doctor, date).
3. Record the result with validity dates (fit / restricted / unfit).
4. The daily cron alerts managers before expiry and can create the
   next periodic visit automatically.

## Permissions

- `sf_occupational_health.group_oh_user` — read/write limited.
- `sf_occupational_health.group_oh_manager` — full access.
- Medical restrictions are not readable by plain users (confidential).
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- hr
- mail

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).