# Investment Management & Portfolios

Manage investment portfolios and lines (stocks, bonds, money market
and term deposits), market-price valuations, dividends and coupon
receipts with computed revenues, maturity alerts for bonds and term
deposits, and PDF performance reports per portfolio.

## Features

- Portfolios per company account, bank, currency and responsible
- Investment lines with security type, ISIN, quantity and prices
- Computed line value and latent gain/loss
- Valuation history by market price and date
- Dividend and coupon incomes with computed amounts
- Sequential numbering (PF-, LIN-, VAL-, INC-)
- Daily maturity alerts (activity deduplicated)
- Maturity marking when the maturity date is reached
- PDF performance and maturity reports
- Dashboard by security type
- Multi-company security groups and record rules

## Installation

Copy the module to your addons path, update the app list and
install **Investment Management & Portfolios**.

## Configuration

Assign the groups in Settings > Users:

- **Investment Management User**: portfolios, lines, valuations,
  incomes and reports.
- **Investment Management Manager**: full access including portfolio
  closure and validation of income receipts.

Company settings (Settings > Investments):
- Maturity alert margin (days).

## Usage

1. Create a portfolio (company account, bank, currency, responsible).
2. Add investment lines: quantity, cost price and current price.
3. Record valuations by market price and date.
4. Record dividends and coupons; the coupon amount is computed as
   quantity x coupon rate when received.
5. The daily cron raises a maturity alert for open bonds and term
   deposits nearing their maturity date and marks lines as matured.
6. Print the PDF performance report from a portfolio or the maturity
   list from an investment line.

## Permissions

- `sf_investment_management.group_invest_user` — read/write limited.
- `sf_investment_management.group_invest_manager` — full access.
- Multi-company record rules restrict users to their company.
- Portfolio closure and income receipt validation are manager-only.

## Dependencies

- base
- mail
- contacts

## Compatibility

Odoo 18.0 (Community and Enterprise).