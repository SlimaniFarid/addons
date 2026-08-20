# Staffing Agency & Placement

Temporary work and placement agency management module for Odoo 18. It manages the full candidate to invoicing cycle for temporary work agencies and placement officers: candidates and profiles, clients and staffing needs, missions and mission contracts, interim worker timesheets and client invoicing from validated timesheets.

## Features

- Candidates with profile, skills, availability and mission history.
- Clients and their staffing needs (position, period, required skills).
- Missions and mission contracts between client, agency and candidate.
- Timesheet tracking for interim workers with hours control (positive hours, maximum 24 per day).
- Client invoicing from validated (done) timesheets only.
- Daily reminder cron activities for missions expiring within the configured delay and for unvalidated timesheets of the previous day (deduplicated TODO activities).
- Multi-company support with per-company record rules; managers see all companies.
- Manager-only reserved actions: cancellation of confirmed missions, modification of contractual rates and final invoice validation.
- PDF reports: mission contract, candidate sheet, mission invoice and activity report.
- Dedicated settings page for the default mission end reminder delay.

## Models

- `sf.staffing.candidate`
- `sf.staffing.client`
- `sf.staffing.need`
- `sf.staffing.mission`
- `sf.staffing.contract`
- `sf.staffing.timesheet`

Sequences are generated automatically: `CAN-`, `CLI-`, `NED-`, `MIS-`, `CTR-`, `TIM-`.

## Workflows

- Candidate: Draft, Available, Assigned, On Mission, Unavailable.
- Mission: Draft, Confirmed, In Progress, Done, Cancelled.
- Timesheet: Draft, Confirmed, Done, Cancelled.
- Contract: Draft, Confirmed, Done, Cancelled.

## Security

Two groups are provided in the `Staffing` category:

- Staffing / User: full business access on all staffing models for their own company.
- Staffing / Manager: reserved actions and visibility across all companies.

## Installation

Install the module from the Apps menu. Dependencies: `base`, `mail`, `contacts`, `account`.

## Configuration

Open Settings > Staffing to configure the default mission end reminder delay in days (default 7).

## License

OPL-1 (Odoo Proprietary License). Author: Ethan Miller. Support: tech5262@gmail.com.