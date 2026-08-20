# Cleaning Services & Contracts

Management of recurring cleaning service contracts: site tracking,
intervention frequencies, agent schedules, quality checks and
service invoicing. Covers the full cycle from contract signature
to invoicing and quality control, with automatic alerts for
missed frequencies or unassigned agents.

## Features

- Recurring cleaning contracts (draft → active → suspended →
  done / cancelled)
- Sites linked to clients with team leader assigned
- Agent schedules and order of mission workflows
- Intervention execution recorded by agents
- Quality checks per intervention validated by the team leader
- Automatic TODO alert cron (deduplicated) for missed
  frequencies and unassigned agents
- Service invoicing from validated interventions (contract rates)
- PDF reports: order of mission and monthly service summary
- Multi-company access rules

## Installation

Copy the module to your addons path, update the app list and
install **Cleaning Services & Contracts**.

## Configuration

Assign the groups in Settings > Users:

- **Cleaning User**: schedules and intervention execution.
- **Cleaning Manager**: contracts, plans, quality checks and
  invoicing.

Company settings (Settings > Cleaning):
- Alert cron, delay threshold and default intervention duration.

## Usage

1. Create a cleaning contract with sites, frequencies and rates.
2. Build agent schedules per site and assign agents.
3. Agents record executed interventions on site.
4. Team leaders validate interventions and quality checks.
5. The cron alerts missed frequencies and unassigned agents.
6. Generate monthly invoicing from validated interventions.

## Permissions

- `sf_cleaning.group_sf_cleaning_user` — read/write on own
  schedule lines.
- `sf_cleaning.group_sf_cleaning_manager` — contracts, plans,
  quality checks and invoicing.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).