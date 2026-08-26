# Warranty & Claims Management

Centralize product warranties (duration, coverage), process customer
claims with automatic eligibility verification (serial number,
purchase date) and motivated decisions with warranty cost tracking.

## Features

- Warranty catalog per product (duration, coverage)
- Claims workflow: draft → open → decision → closed / rejected
- Automatic eligibility check (serial number + purchase date)
- Motivated decisions with mandatory reason on rejection
- Estimated warranty cost per claim
- Warranty page on the product form
- Dashboard of claims by state and decision

## Installation

Copy the module into your addons path, update the apps list and
install **Warranty & Claims Management**.

## Configuration

Settings → General Settings → Warranty Management:

- **Check eligibility when opening a claim**: enable automatic
  eligibility verification at claim opening.

Define warranties under **Warranty & Claims → Product Warranties**,
then record claims under **Warranty & Claims → Claims**.

## Permissions

- **Warranty Management User**: record and process claims of their
  own company.
- **Warranty Management Manager**: everything, including warranty
  catalog, decisions and multi-company access.

## Dependencies

- base
- mail
- product
- stock
- sale
- account

## Compatibility

- Odoo 18.0 and 19.0
- Community and Enterprise