# Litigation & Legal Case Management

Manage legal matters and pre-litigation: cases and parties, legal
domains, procedural deadlines with alerts, fees and honoraries,
decisions and results, and a legal activity PDF report.

## Features

- Litigation cases with parties (plaintiff, defendant, third parties)
  and legal domains (commercial, social, fiscal, civil, criminal)
- Sequential numbering (LIT-/DDL-/FEE-/DEC-xxxx)
- Procedural deadlines with alert activities via daily cron
  (configurable alert delay per company)
- Fees and honoraries per case (lawyer, court, expert, travel)
- Decisions, outcomes and controlled case closure (decision or
  closing reason required, manager only)
- Legal activity report and case sheet (PDF)
- Multi-company record rules and manager groups
- Dashboard of cases by legal domain and status

## Installation

Copy the module to your addons path, update the app list and
install **Litigation & Legal Case Management**.

## Configuration

Assign the groups in Settings > Users:

- **Litigation User**: cases, deadlines, fees, decisions.
- **Litigation Manager**: full access including case closure and all
  companies.

Company settings (Settings > Litigation):
- Deadline alert delay (days).

## Usage

1. Create a case with the parties and the legal domain.
2. Open the case, then mark it pending once the procedure starts.
3. Register procedural deadlines; the cron schedules alert
   activities and flags missed deadlines.
4. Record fees and honoraries on the case.
5. Record a decision (or a closing reason), then close the case
   (manager only).
6. Print the Legal Activity Report or the Case Sheet (PDF).

## Permissions

- `sf_litigation.group_litigation_user` — read/write on own company.
- `sf_litigation.group_litigation_manager` — full access, all
  companies, case closure.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).