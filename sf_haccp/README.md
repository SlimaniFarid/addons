# HACCP Food Safety

Sanitary compliance for restaurants, food industry and
distribution: HACCP plans (prerequisites, CCP with critical
limits), monitoring checks (temperature, cleaning) with automatic
deviation detection and corrective actions, nonconformity register
and auditable HACCP PDF registers per site.

## Features

- Sites and prerequisite management (cleaning, water, pest,
  training, waste, storage)
- HACCP plans by process/zone with steps, hazards, CCP and
  critical limits
- Planned monitoring checks (temperature, cleaning, pH) with
  results and automatic status
- Automatic deviation detection out of [target_min, target_max]
  and nonconformity creation
- Corrective actions and manager-only closure of nonconformities
- Daily cron alerts for scheduled checks without result and
  overdue nonconformities
- Auditable HACCP PDF register per site
- Multi-company record rules

## Installation

Copy the module to your addons path, update the app list and
install **HACCP Food Safety**.

## Configuration

Assign the groups in Settings > Users:

- **HACCP User**: record checks and prerequisite status.
- **HACCP Manager**: full access (sites, plans, configuration,
  closing nonconformities).

Company settings (Settings > HACCP Food Safety):
- Control reminder margin (days) before a scheduled check without
  a result raises an alert.

## Usage

1. Create sites and their prerequisites (cleaning, pest, training...).
2. Create HACCP plans per process/zone with steps, hazards, CCP
   and critical limits.
3. Record monitoring checks (temperature, cleaning, pH) with
   results; the check automatically deviates when the result is
   outside the critical range and creates a nonconformity.
4. Fill the corrective action, respect the due date and close the
   nonconformity (manager only); the linked check is resolved.
5. Generate the auditable HACCP register PDF per site.

## Permissions

- `sf_haccp.group_haccp_user` — record checks and prerequisites.
- `sf_haccp.group_haccp_manager` — full access, closing of
  nonconformities.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts
- hr

## Compatibility

Odoo 18.0 (Community and Enterprise).