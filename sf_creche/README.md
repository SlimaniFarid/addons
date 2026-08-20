# Creche Management

Centralize children records, enrollments with schedules, daily
attendance with arrival/departure times, rooms with capacity
control and monthly billing computed on real attended hours.

## Features

- Children records (identity, birth date, parents, allergies)
- Sequential numbering for children, enrollments, attendance, rooms
  and billing
- Enrollments with schedule (full time / half day)
- Daily attendance with arrival and departure times
- Room capacity check at attendance close
- Monthly billing based on real hours x hourly rate
- End-date reminder alerts via cron (deduplicated)
- PDF monthly invoice and attendance register reports
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Creche Management**.

## Configuration

Assign the groups in Settings > Users:

- **Creche User**: children, attendance and rooms.
- **Creche Manager**: full access, enrollments and billing, all
  companies.

Company settings (Settings > Creche):
- Default hourly rate.
- Number of days before an ending enrollment is alerted.

## Usage

1. Create children records and rooms with capacity.
2. Enroll a child with a schedule and a room.
3. Record daily attendance (arrival / departure).
4. Close the attendance; the capacity check runs.
5. Generate the monthly billing from the attended hours.

## Permissions

- `sf_creche.group_sf_creche_user` — read/write limited.
- `sf_creche.group_sf_creche_manager` — full access, enrollments and
  billing.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).