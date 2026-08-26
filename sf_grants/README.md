# Grants & Public Funding Management

Manage subsidies and public funding: programs and calls for projects,
application files with a full workflow, justified expenses attached to
each application and auditable financial reports per program.

## Features

- Programs and calls for projects (funder, budget, deadlines)
- Sequential numbering (PRG-, CAL-, APP-, EXP-)
- Application workflow: draft → submitted → approved → paid → closed
  or rejected
- Manager-only approvals, payments, closures and rejections
- Justified expenses with budget control (validated expenses cannot
  exceed the granted amount)
- Daily cron deadline and reporting alerts (activity dedup)
- Financial report per program (PDF)
- Aid register (PDF) auditable
- Dashboard of applications by funder type

## Installation

Copy the module to your addons path, update the app list and
install **Grants & Public Funding Management**.

## Configuration

Assign the groups in Settings > Users:

- **Grants User**: create programs, calls, applications and expenses.
- **Grants Manager**: full access (approvals, payments, closures,
  expense validation).

Company settings (Settings > Grants):
- Grant deadline alert margin (days).

## Usage

1. Create a funding program (funder, funder type).
2. Create a call for projects and open it.
3. Submit applications (a call and a requested amount are required).
4. Managers approve, pay and close applications.
5. Attach justified expenses; managers validate them within the
   granted amount.
6. Use the Financial Report per program and the Aid Register for
   audits. The daily cron raises deadline and reporting alerts.

## Permissions

- `sf_grants.group_grant_user` — read/write limited.
- `sf_grants.group_grant_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).