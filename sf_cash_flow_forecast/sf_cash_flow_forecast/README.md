# Cash Flow & Treasury Manager

Forecast your cash position, track receivables and payables, and avoid liquidity gaps.

## Features

- Rolling cash position: opening balance plus expected inflows and outflows
- Automatic inflow forecast from open customer invoices by due date
- Automatic outflow forecast from open vendor bills and confirmed purchase orders
- Manual cash flow lines: planned payments, loans, transfers, investments
- Configurable horizon (7, 30, 60, 90, 180 days)
- Low-balance alerts with threshold warnings
- Projected minimum balance and date
- Automatic lines regenerable from accounting data at any time
- Works with native Odoo accounting (no configuration required)

## Installation

Install the module from Apps. Open the **Accounting** app then **Cash Flow** menu.

## Usage

1. Open **Accounting > Cash Flow > Cash Flow Forecasts**.
2. Create a forecast: set start date, horizon and the bank/cash journals to include.
3. Click **Generate Lines** to pull receivables, payables and purchase orders.
4. Optionally add manual lines (planned payments, loans...).
5. Set an **Alert Threshold** and click **Confirm** to activate alerts.
6. Review projected totals, minimum balance and the alert list.

## Known Limitations

- Projection is a snapshot: use **Generate Lines** to refresh it.
- Purchase order outflows use the full order amount (not yet-invoiced only).

## License

OPL-1 — proprietary license. Support: tech5262@gmail.com