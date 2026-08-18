# Construction BOQ & Subcontractor Billing

## Description

Manage construction projects with Bills of Quantities (BOQ), subcontracts and progress billing (Interim Payment Certificates / IPC). Built for contractors, main contractors and construction project managers.

## Problem solved

Construction companies manage estimates, subcontracts and progress certificates in spreadsheets. This module brings a structured, reliable and multi-company ready workflow inside Odoo with automatic amount calculations and a printable certificate report.

## Features

- Bill of Quantities with multi-discipline lines (earthwork, concrete, masonry, structure, finishing, electrical, plumbing, HVAC, roofing, other)
- BOQ workflow: Draft → Confirmed → In Progress → Done / Cancelled
- Subcontracts with contractor, contract amount, retention rate, advance and dates
- Subcontract workflow: Draft → Confirmed → In Progress → Closed / Cancelled
- Payment certificates (IPC) with period, previous quantity, current quantity and unit price per line
- Automatic computations: previously certified, current period, retention, net amount, amount to pay
- Certificate workflow: Draft → Confirmed → Paid / Cancelled
- PDF report for payment certificates
- Chatter (tracking, activities, messages) on all main models

## Installation

1. Copy the `sf_construction_boq` folder into your addons path.
2. Update the apps list (Apps → Update Apps List).
3. Install "Construction BOQ & Subcontractor Billing".

## Configuration

No configuration is required. Users in the "Construction / Manager" group can create, confirm and manage records. Users in the "Construction / User" group have read-only access.

## Usage

1. Create a project (Project app) for the construction site.
2. Create a Bill of Quantities and add itemized lines per discipline.
3. Confirm the BOQ, then start it.
4. Create subcontracts for each contractor, setting contract amount, retention rate and advance.
5. From a confirmed/in-progress subcontract, click "Create Payment Certificate".
6. Fill the certificate lines with period work done and confirm.
7. Print the PDF or mark the certificate as paid.

## Permissions

- **Construction / User**: read access on BOQs, subcontracts and certificates.
- **Construction / Manager**: full CRUD and workflow control.

## Dependencies

- base
- project
- product
- account
- uom

## Compatibility

Odoo 18.0 and 19.0 (two separate branches).

## Support

Support email: tech5262@gmail.com