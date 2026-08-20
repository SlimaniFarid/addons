# Export Documents & Customs Compliance

Manage export dossiers: generate the export document pack
(commercial invoice, packing list, certificate of origin,
EUR.1 / ATR), manage Incoterms, ports and countries of origin,
check completeness before shipment and archive the history.

## Features

- Export dossier workflow: draft → in_preparation → ready → shipped → archived
- Incoterms reference and transport modes
- Commercial invoice and packing list from the sale order
- Certificate of origin and EUR.1 / ATR reports
- Completeness control before shipment (4 documents)
- Overdue preparation alerts via cron
- Dashboard of dossiers by state and destination

## Installation

Copy the module into your addons path, update the apps list and
install **Export Documents & Customs Compliance**.

## Configuration

Settings → General Settings → Export Documents:

- **Default country of origin**: applied to new dossiers.
- **Export preparation alert (days)**: delay before alerting on
  dossiers still in preparation.

Create your dossiers under **Export Documents → Export Dossiers**,
generate the document pack and mark the dossier ready, then shipped.

## Permissions

- **Export Documents User**: create dossiers and generate documents
  for their own company.
- **Export Documents Manager**: everything, including Incoterms
  management and multi-company access.

## Dependencies

- base
- mail
- contacts
- sale
- product

## Compatibility

- Odoo 18.0 and 19.0
- Community and Enterprise