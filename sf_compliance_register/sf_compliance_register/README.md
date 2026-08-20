# Compliance Documents & Licenses Register

Central register for all company documents that expire: licenses,
permits, certifications, agreements and insurance.

## Features

- Centralized document register with types and categories
- Responsible owner per document
- Automatic expiry status (active / expiring / expired)
- Automatic renewal alerts (email activities via daily cron)
- Renewal workflow with full history and old document archival
- Attachments per document
- Compliance dashboard and reports

## Installation

Copy the module to your addons path, update the app list and
install **Compliance Documents & Licenses Register**.

## Configuration

Assign the groups in Settings > Users:

- **Compliance User**: create draft documents and renew.
- **Compliance Manager**: full access (publication, types,
  history, configuration).

Company settings (Settings > Compliance Register):
- Default alert days.
- Require attachment at publication (optional).

## Usage

1. Create a document type (license, permit, insurance, etc.).
2. Create documents with issue/expiry dates, attach files and
   assign a responsible person.
3. Publish: the status is computed automatically.
4. The daily cron schedules renewal activities before expiry.
5. Renew from the document form: a new version is created and
   the previous one is archived.

## Permissions

- `sf_compliance_register.group_compliance_user` — read/write limited.
- `sf_compliance_register.group_compliance_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- mail

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).