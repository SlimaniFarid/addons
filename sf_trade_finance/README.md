# Trade Finance — LC & Bank Guarantees

Manage international documentary payment instruments: letters of
credit (import/export), bank guarantees and documentary
collections, with key dates, required documents, bank fees and
links to orders and invoices.

## Features

- Instruments: import/export LC, bank guarantees, collections
- Sequential numbering per type (LC-, ELC-, BG-, DC-)
- Key dates (application, issue, expiry, payment) with daily
  expiry alerts (configurable threshold)
- Required documents with submit / accept / reject workflow
- Settle blocked until all documents are accepted
- Bank fees register per instrument
- Links to purchase orders and invoices
- Dashboard of outstanding amounts and expiring instruments

## Installation

Copy the module to your addons path, update the app list and
install **Trade Finance — LC & Bank Guarantees**.

## Configuration

Assign the groups in Settings > Users:

- **Trade Finance User**: consult instruments, create and update
  documents.
- **Trade Finance Manager**: full access, close/cancel,
  configuration, dashboard.

Company settings (Settings > Trade Finance):
- Expiry alert threshold (days).

## Usage

1. Create a bank (menu Banks).
2. Create an instrument with its type, direction, bank,
   counterparty, currency and amount.
3. Follow the workflow: request → issue → activate → settle → close.
4. Add required documents and update their status.
5. Link the instrument to purchase orders and invoices.
6. The daily cron alerts the treasury before expiry.

## Permissions

- `sf_trade_finance.group_trade_user` — read/write limited.
- `sf_trade_finance.group_trade_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- sale
- purchase
- account
- mail

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).