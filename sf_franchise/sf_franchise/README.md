# SF Franchise

Retail Franchise Network Management module for Odoo 18.

## Features

- Franchise contracts with territory and royalty conditions (fixed amount or percentage of declared sales).
- Periodic sales declarations by franchisees with automatic royalty calculation.
- Royalty invoicing through `account.move` (posted out invoices) with configurable income account and sale journal.
- Payment and delay tracking through the related invoice.
- Full workflow: contract draft / active / suspended / terminated; declaration draft / confirmed / invoiced / paid / cancelled.
- Daily cron that raises reminders for confirmed declarations awaiting invoicing and unpaid royalty invoices.
- Multi-company support with record rules per company.
- QWeb PDF reports: Franchise Contract and Royalty Statement.

## Configuration

In Settings &gt; Franchise you can configure:

- Default royalty income account (falls back to the first income account of the company).
- Default sale journal (falls back to the first sale journal of the company).

## Usage

1. Create a franchise contract for a franchisee with its royalty conditions.
2. Activate the contract, then create sales declarations for each period (declared sales are entered, not computed from the POS/sales).
3. A manager confirms the declaration (royalty is computed automatically), generates the royalty invoice and marks it as paid once settled.
4. The daily cron raises reminders for pending invoicing and unpaid invoices.

## Permissions

- `sf_franchise.group_sf_franchise_user` - day-to-day operations.
- `sf_franchise.group_sf_franchise_manager` - confirmation, invoicing, payment marking, cancellation and contract closure.

## Dependencies

`base`, `mail`, `contacts`, `account`.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.