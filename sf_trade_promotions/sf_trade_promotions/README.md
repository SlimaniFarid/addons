# Trade Promotion Management (TPM)

Trade promotion programs, budgets, customer claims, validation workflow and ROI tracking for Odoo 18.

## Features

- Promotion programs with a budget, promotion type, period and eligible customers.
- Customer claims / deductions recording, submission and validation workflow.
- Automatic budget consumption tracking (total claimed, remaining budget).
- ROI computation per program (budget utilization percentage).
- Manager-gated validation, payment, closure and cancellation.
- Daily cron that closes active programs whose end date has passed.
- Validation threshold: claims above the configured amount trigger a review activity.
- Multi-company support with record rules per company.
- QWeb PDF reports: Trade Programs and Trade Promotion Claims.

## Configuration

In Settings &gt; Trade Promotions you can configure:

- Validation threshold (claims above this amount raise a review activity on submission; 0 disables it).
- Product account (reserved for future integration).

## Usage

1. Create a trade program with a budget, period and eligible customers.
2. Activate the program when it starts.
3. Record customer claims (amount and related invoice) and submit them.
4. A manager approves (budget is enforced), rejects, or marks claims as paid.
5. The daily cron automatically closes programs past their end date; managers can also close or cancel programs.

## Permissions

- `sf_trade_promotions.group_sf_trade_promotions_user` - create programs and claims, activate programs and submit claims.
- `sf_trade_promotions.group_sf_trade_promotions_manager` - approve, reject, pay, cancel claims and close or cancel programs.

## Dependencies

`base`, `mail`, `contacts`, `account`.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.