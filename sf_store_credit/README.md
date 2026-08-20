# SF Store Credit

Retail Store Credit &amp; Customer Wallet module for Odoo 18.

## Features

- Customer credit accounts (one account per customer and company).
- Reusable store credits with reason, amount and expiration date.
- Automatic balance calculation per account.
- Partial or full credit usage on sales (no accounting entries are created).
- Manager-gated confirmation, cancellation and adjustments (with a dedicated adjustment wizard).
- Full movement history per credit (grant, use, adjustment, expiration, cancellation).
- Daily cron that expires confirmed credits past their expiration date and raises reminders before expiration.
- Multi-company support with record rules per company.
- QWeb PDF reports: Customer Balances and Store Credit.

## Configuration

In Settings &gt; Store Credit you can configure:

- Expiry reminder delay (in days) before a credit expires.

## Usage

1. Create a credit account for a customer.
2. Grant a credit with a reason and an optional expiration date; a manager confirms it.
3. At the counter, check the available balance and use the credit on a sale (partial or full).
4. A manager can record an adjustment to correct the balance or cancel an unused credit.
5. The daily cron expires credits past their expiration date and raises reminders for upcoming expirations.

## Permissions

- `sf_store_credit.group_sf_store_credit_user` - view accounts and credits, grant credits and use them.
- `sf_store_credit.group_sf_store_credit_manager` - confirm, adjust and cancel credits.

## Dependencies

`base`, `mail`, `contacts`, `sale`.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.