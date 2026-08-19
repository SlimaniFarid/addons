# Business Continuity & BIA (PCA)

Manage the company resilience program (ISO 22301): critical processes
with a Business Impact Analysis (criticality, RTO, RPO and financial
impact), continuity strategies, recovery plans with steps and owners,
exercises with results and automatic review reminders.

## Features

- Business Impact Analysis: critical processes with RTO / RPO
- Criticality levels (critical, important, normal) and financial impact
- Continuity strategies (alternate site, workaround, outsourcing,
  manual, staffing)
- Recovery plans: version, summary, steps, resources, owner
- Plan workflow: draft, published, tested, updated
- Exercises and tests with results and improvement findings
- Periodic plan review alerts via daily cron (configurable interval)
- BIA and Recovery Plan PDF reports
- Dashboard by criticality and status

## Installation

Copy the module to your addons path, update the app list and install
**Business Continuity & BIA (PCA)**.

## Configuration

Assign the groups in Settings > Users:

- **Business Continuity User**: register processes, strategies, plans
  and exercises.
- **Business Continuity Manager**: full access; validates BIA and
  publishes plans.

Company settings (Settings > Business Continuity):
- Plan review interval (days, default 365).

## Usage

1. Create critical processes with criticality, RTO, RPO and impact.
2. Assess, then let a manager validate the BIA.
3. Define continuity strategies per process.
4. Write the recovery plan (summary and steps) and publish it.
5. Run exercises, record results and mark them done.
6. The daily cron raises a review reminder when a plan is due.

## Permissions

- `sf_business_continuity.group_bcp_user` — read/write limited.
- `sf_business_continuity.group_bcp_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).