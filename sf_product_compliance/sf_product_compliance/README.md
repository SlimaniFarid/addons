# Product Compliance & Technical Documentation

Regulatory compliance of products (CE, RoHS, REACH, UL, FDA):
regulations reference, requirements per product, compliance
dossiers with documents and validations, certificates with
expiry dates and alerts, compliance status by market.

## Features

- Regulation / market reference with mandatory flag
- Sequential numbering (REG-, REQ-, DOS-, CER-)
- Product requirements with evidence and satisfaction tracking
- Compliance dossiers with validation workflow and attachments
- Certificates with expiry dates and automatic alerts (cron)
- Computed product compliance status
- PDF compliance report per product
- Expired certificates report
- Dashboard of dossiers by state and regulation

## Installation

Copy the module to your addons path, update the app list and
install **Product Compliance & Technical Documentation**.

## Configuration

Assign the groups in Settings > Users:

- **Compliance User**: manage regulations, requirements, dossiers
  and certificates.
- **Compliance Manager**: full access and validation rights
  (dossier review, requirement satisfaction, cross-company).

Company settings (Settings > Product Compliance):
- Certificate expiry alert delay (days).

## Usage

1. Create the regulations / markets (CE, RoHS, REACH, ...).
2. Attach compliance requirements to each product.
3. Create a compliance dossier per (product, regulation) and send
   it to review.
4. Mark the product requirements satisfied; the dossier can then
   be marked compliant.
5. Record certificates with expiry dates; the daily cron expires
   them and raises reminder / expiry activities.
6. Use the PDF reports and the dashboard for audits.

## Permissions

- `sf_product_compliance.group_compliance_user` — read/write/create.
- `sf_product_compliance.group_compliance_manager` — full access
  and validation.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail
- product
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).