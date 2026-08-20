# Corporate Secretary & Corporate Life

Manage the corporate life of the company: organs (general meetings,
board of directors), convocations and tracked sending, assemblies
with resolutions and votes, proxies, minutes (PV), written decisions
(simplified procedure), representatives and mandates, and the
regulatory deadlines agenda per company.

## Features

- Organ registry (AGA, AGE, board, supervisory board) with
  chairperson, members and notice periods
- Sequential numbering: ORG- / MEE- / RES- / DEC- / FOR-
- Assembly workflow: planned -> in progress -> done -> archived
- Convocation workflow: draft -> sent -> held -> minutes done
- Resolutions with votes and automatic adoption rule
- Meeting minutes (PV) PDF report with votes and adoption
- Written decisions: draft -> signed -> filed
- Regulatory formality schedule with PDF report
- Daily cron generating activities for upcoming deadlines
- Multi-company record rules and manager-only closures

## Installation

Copy the module to your addons path, update the app list and
install **Corporate Secretary &amp; Corporate Life**.

## Configuration

Assign the groups in Settings > Users:

- **Corporate Secretary User**: manage organs, meetings, resolutions,
  decisions and formalities for their own company.
- **Corporate Secretary Manager**: full access, including closing
  meetings and seeing all companies.

Company settings (Settings > Corporate Secretary):
- Default notice period (days) for convocations.

## Usage

1. Create the organs (AGA, AGE, board) with chairperson and members.
2. Schedule a meeting: the notice date is computed automatically.
3. Send the convocation and mark it as sent; hold the meeting.
4. Enter the resolutions and votes, then write the minutes (PV).
5. Close the meeting as a manager (minutes are mandatory).
6. Track written decisions (draft -> signed -> filed).
7. Monitor regulatory formalities and the daily deadline alerts.

## Permissions

- `sf_corporate_secretary.group_corporate_user` — read/write limited.
- `sf_corporate_secretary.group_corporate_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).