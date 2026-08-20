# Bank Loans & Credits

Track bank financing: loan files (bank, amount, rate, term),
calculated amortization schedules (annuity or constant), drawdowns
and early repayments, covenants with breach alerts, debt projection
and a debt position report by bank.

## Features

- Banks and contacts (linked partners)
- Sequential loan numbering (LOA-xxxx) with dedicated sequences
  for banks, drawdowns, repayments and covenants
- Loan files with workflow: draft → offered → disbursing → active
  → closed
- Amortization schedule generation (annuity or constant) with a
  last-line adjustment so principal always sums exactly to the amount
- Drawdowns that update the disbursed capital and regenerate the
  remaining schedule
- Early repayments that adjust the remaining debt
- Covenants with target range, breach detection and review
- Daily cron that alerts breached covenants and overdue installments
  (configurable delay)
- Amortization schedule PDF and debt position PDF by bank
- Debt dashboard (loans by bank and by status)

## Installation

Copy the module to your addons path, update the app list and
install **Bank Loans & Credits**.

## Configuration

Assign the groups in Settings > Users:

- **Bank Loans User**: create banks, loans, drawdowns and
  repayments; track covenants.
- **Bank Loans Manager**: full access (close loans, validate early
  repayments, all companies).

Company settings (Settings > Bank Loans):
- Loan alert delay (days): number of days after the due date before
  an unpaid installment raises an overdue alert.

## Usage

1. Create a bank (optional linked partner).
2. Create a loan and generate the amortization schedule.
3. Register drawdowns as the capital is disbursed.
4. Confirm early repayments when applicable.
5. Record covenants and let the daily cron raise breach alerts.
6. Print the amortization schedule or the debt position report by
   bank; use the dashboard to review the debt.

## Permissions

- `sf_bank_loans.group_loan_user` — read/write limited.
- `sf_bank_loans.group_loan_manager` — full access.
- Multi-company record rules restrict users to their company;
  managers see all companies.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).