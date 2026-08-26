# Employee Onboarding & Offboarding

Automate structured arrival and departure journeys for employees
with templates, task checklists, owners and reminders.

## Features

- Onboarding and offboarding journey templates
- Automatic program generation when an employee is created
- Tasks with owners, due dates and statuses
- Required / optional tasks
- Progress tracking and kanban board
- Equipment preparation and return checks
- Completion notes and audit trail
- Automatic reminders for late tasks (daily cron)

## Installation

Copy the module to your addons path, update the app list and
install **Employee Onboarding & Offboarding**.

## Configuration

Assign the groups in Settings > Users:

- **Onboarding User**: view programs, manage assigned tasks.
- **Onboarding Manager**: full access (templates, generation,
  programs, configuration).

Company settings:
- Default onboarding template.
- Default offboarding template.

## Usage

1. Create onboarding/offboarding templates with tasks.
2. Set a default template per company, or generate a program
   manually from the Onboarding > Generate Program menu.
3. Track programs in the kanban board and complete tasks.
4. The daily cron schedules reminders for late tasks.

## Permissions

- `sf_hr_onboarding.group_onboarding_user` — read/write limited.
- `sf_hr_onboarding.group_onboarding_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- hr

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).