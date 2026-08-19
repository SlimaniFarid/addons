# Waste Management (BSD)

Manage waste tracking slips (BSD) with production sites, waste codes
and a complete emission, transfer and reception workflow. Track
hazardous and non-hazardous waste quantities per code and site and
alert the site manager when a reception is overdue.

## Features

- BSD workflow: draft → emitted → transferred → received → archived
- Waste sites and waste codes (with hazardous flag)
- Collectors and destination partners
- Overdue reception alerts via cron
- Dashboard of quantities by waste code and site

## Installation

Copy the module into your addons path, update the apps list and
install **Waste Management (BSD)**.

## Configuration

Settings → General Settings → Waste Management:

- **Waste reception alert (days)**: delay after the expected reception
  date before alerting the site manager.

Create your sites and waste codes, then register your BSDs under
**Waste Management → Waste Tracking Slips (BSD)**.

## Permissions

- **Waste Management User**: create and follow slips for their own
  company.
- **Waste Management Manager**: everything, including sites and codes
  management and multi-company access.

## Dependencies

- base
- mail
- contacts

## Compatibility

- Odoo 18.0 and 19.0
- Community and Enterprise